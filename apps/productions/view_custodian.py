import pandas as pd
import io
import re
import os
import json
from flask import g, make_response, request

from bases.viewhandler import ApiViewHandler
from bases.globals import db, settings
from bases.exceptions import VerifyError, LogicError
from models import FOFNavCalc, HedgeFundCustodianData, FOFPosition, HedgeFundInvestorDivAndCarry, \
    HedgeFundInvestorPurAndRedemp, UnitMap
from utils.decorators import login_required
from utils.helper import replace_nan
from utils.serializer import DataFrameDictSerializer
from utils.xlsx2html import xlsx2html
from utils.caches import get_fund_cache
from extensions.s3.private_file_store import FileStore

from surfing.data.manager.manager_hedge_fund import HedgeFundDataManager
from surfing.constant import FOFTradeStatus
from openpyxl import load_workbook
from xls2xlsx import XLS2XLSX


class NavCompare(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        calc = db.session.query(
            FOFNavCalc.datetime,
            FOFNavCalc.nav,
            FOFNavCalc.mv,
            FOFNavCalc.volume,
        ).filter(
            FOFNavCalc.manager_id == g.token.manager_id,
            FOFNavCalc.fof_id == fof_id,
        ).order_by(FOFNavCalc.datetime.desc()).all()

        cal_df = pd.DataFrame([{
            'datetime': i[0],
            'nav': i[1],
            'mv': i[2],
            'volume': i[3],
        } for i in calc])

        if len(cal_df) < 1:
            return {
                'page': 1,
                'page_size': 10,
                'count': 0,
                'results': [],
            }
        df = cal_df.set_index('datetime')

        cus = db.session.query(
            HedgeFundCustodianData.datetime,
            HedgeFundCustodianData.nav,
            HedgeFundCustodianData.equity,
            HedgeFundCustodianData.total_shares,
            HedgeFundCustodianData.url,
        ).filter(
            HedgeFundCustodianData.manager_id == g.token.manager_id,
            HedgeFundCustodianData.fof_id == fof_id,
        ).all()
        cus_df = pd.DataFrame([{
            'datetime': i[0],
            'cus_nav': i[1],
            'cus_mv': i[2],
            'cus_volume': i[3],
            'url': i[4],
        } for i in cus])
        cus_df = cus_df.set_index('datetime')
        cus_df = cus_df.reindex(df.index)
        df['cus_nav'] = cus_df['cus_nav']
        df['cus_mv'] = cus_df['cus_mv']
        df['cus_volume'] = cus_df['cus_volume']
        df['url'] = cus_df['url']

        df = df.reset_index()
        df = df.sort_values('datetime', ascending=False)

        s = DataFrameDictSerializer()
        data = s.to_representation(df)

        return replace_nan(data)


class CalcPosition(ApiViewHandler):
    @login_required
    def get(self, fof_id, date_str):
        """估算持仓"""
        p = db.session.query(
            FOFPosition
        ).filter(
            FOFPosition.manager_id == g.token.manager_id,
            FOFPosition.fof_id == fof_id,
            FOFPosition.datetime == date_str,
        ).first()

        if not p:
            return {}

        data = dict()
        fund_dict = get_fund_cache()
        position = p.to_dict().get('position')
        position = position or '[]'
        position = json.loads(position)
        for i in position:
            i['fund_name'] = fund_dict.get(i['fund_id'])

        data['position'] = position
        return data


class CusPosition(ApiViewHandler):
    @login_required
    def get(self, fof_id, date_str):
        """托管持仓"""
        p = db.session.query(
            HedgeFundCustodianData
        ).filter(
            HedgeFundCustodianData.manager_id == g.token.manager_id,
            HedgeFundCustodianData.fof_id == fof_id,
            HedgeFundCustodianData.datetime == date_str,
        ).first()

        if not p:
            return {}
        fund_dict = get_fund_cache()

        data = dict()
        data['other_equity'] = p.to_dict()

        hedge_funds_data = data['other_equity']['hedge_funds_data'] or '[]'
        hedge_funds_data = json.loads(hedge_funds_data)
        for i in hedge_funds_data:
            i['fund_name'] = fund_dict.get(i['fund_id'])

        mutual_funds_data = data['other_equity']['mutual_funds_data'] or '[]'
        mutual_funds_data = json.loads(mutual_funds_data)
        for i in mutual_funds_data:
            i['fund_name'] = fund_dict.get(i['fund_id'])

        data['other_equity'].pop('hedge_funds_data')
        data['other_equity'].pop('mutual_funds_data')

        position = hedge_funds_data + mutual_funds_data
        data['position'] = position
        return data


class CalcTrades(ApiViewHandler):

    def calc_pur_redeem(self, fof_id, date_str):
        r = db.session.query(
            HedgeFundInvestorPurAndRedemp
        ).filter(
            HedgeFundInvestorPurAndRedemp.manager_id == g.token.manager_id,
            HedgeFundInvestorPurAndRedemp.fof_id == fof_id,
            HedgeFundInvestorPurAndRedemp.datetime <= date_str,
        ).all()
        if len(r) < 1:
            return {}

        df = pd.DataFrame([i.to_dict() for i in r])

        data = dict()
        purchase = df[df['event_type'].isin([FOFTradeStatus.PURCHASE, FOFTradeStatus.SUBSCRIBE])]

        data['purchase_share'] = purchase['share_changed'].sum()
        data['purchase_detail'] = []
        for i in set(list(purchase['investor_id'])):
            d = dict()
            inv = purchase[purchase['investor_id'] == i]
            d['share'] = inv['share_changed'].sum()
            d['investor_id'] = i
            u = UnitMap.filter_by_query(
                manager_id=g.token.manager_id,
                investor_id=i,
            ).first()
            if u:
                d['investor_name'] = u.name
                d['investor_mobile'] = u.mobile
            d['detail'] = inv[['share_changed', 'datetime']].to_dict(orient='records')
            data['purchase_detail'].append(d)

        redeem = df[df['event_type'] == FOFTradeStatus.REDEEM]
        data['redeem_share'] = redeem['share_changed'].sum()
        data['redeem_detail'] = []
        for i in set(list(redeem['investor_id'])):
            d = dict()
            inv = redeem[redeem['investor_id'] == i]
            d['share'] = inv['share_changed'].sum()
            d['investor_id'] = i
            u = UnitMap.filter_by_query(
                manager_id=g.token.manager_id,
                investor_id=i,
            ).first()
            if u:
                d['investor_name'] = u.name
                d['investor_mobile'] = u.mobile
            d['detail'] = inv[['share_changed', 'datetime']].to_dict(orient='records')
            data['redeem_detail'].append(d)
        return data

    def calc_div_car(self, fof_id, date_str):
        r = db.session.query(
            HedgeFundInvestorDivAndCarry
        ).filter(
            HedgeFundInvestorDivAndCarry.manager_id == g.token.manager_id,
            HedgeFundInvestorDivAndCarry.fof_id == fof_id,
            HedgeFundInvestorDivAndCarry.datetime <= date_str,
        ).all()
        if len(r) < 1:
            return {}

        df = pd.DataFrame([i.to_dict() for i in r])

        data = dict()
        dividend = df[df['event_type'].isin([FOFTradeStatus.DIVIDEND_VOLUME, FOFTradeStatus.DIVIDEND_CASH])]

        data['dividend_share'] = dividend['share_changed'].sum()
        data['dividend_detail'] = []
        for i in set(list(dividend['investor_id'])):
            d = dict()
            inv = dividend[dividend['investor_id'] == i]
            d['share'] = inv['share_changed'].sum()
            d['investor_id'] = i
            u = UnitMap.filter_by_query(
                manager_id=g.token.manager_id,
                investor_id=i,
            ).first()
            if u:
                d['investor_name'] = u.name
                d['investor_mobile'] = u.mobile
            d['detail'] = inv[['share_changed', 'datetime']].to_dict(orient='records')
            data['dividend_detail'].append(d)

        reward = df[df['event_type'] == FOFTradeStatus.DEDUCT_REWARD]
        data['reward_share'] = reward['share_changed'].sum()
        data['reward_detail'] = []
        for i in set(list(reward['investor_id'])):
            d = dict()
            inv = reward[reward['investor_id'] == i]
            d['share'] = inv['share_changed'].sum()
            d['investor_id'] = i
            u = UnitMap.filter_by_query(
                manager_id=g.token.manager_id,
                investor_id=i,
            ).first()
            if u:
                d['investor_name'] = u.name
                d['investor_mobile'] = u.mobile
            d['detail'] = inv[['share_changed', 'datetime']].to_dict(orient='records')
            data['reward_detail'].append(d)
        return data

    @login_required
    def get(self, fof_id, date_str):
        """估算交易记录"""
        data = {}
        pur_redeem = self.calc_pur_redeem(fof_id, date_str)
        div_carry = self.calc_div_car(fof_id, date_str)
        data.update(pur_redeem)
        data.update(div_carry)
        return replace_nan(data)


class UploadCusNav(ApiViewHandler):

    @login_required
    def post(self, fof_id):
        """上传托管净值文件"""
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        file_obj = request.files.get('file')

        if not file_obj:
            raise VerifyError('没有文件！')

        # 1、验证文件
        file_suffix = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', file_obj.filename)[0]
        file_name = os.path.join(settings['TEMP_PATH'], f'file_from_user_{g.user.id}{file_suffix}')
        if file_suffix == '.xls':
            FileStore().load_from_user(file_obj, file_name)
            x2x = XLS2XLSX(file_name)
            FileStore.clear_temp_file(file_name)
            file_name = f'{file_name}x'
            x2x.to_xlsx(file_name)
            file_suffix = '.xlsx'
        elif file_suffix == '.xlsx':
            FileStore().load_from_user(file_obj, file_name)
        else:
            raise VerifyError('暂不支持此文件格式！')

        # 2、储存数据到数据库
        hf = HedgeFundDataManager()
        with open(file_name, 'rb') as f:
            date = hf.upload_custodian_data(
                manager_id=g.token.manager_id,
                fof_id=fof_id,
                datas=f,
            )

        # 3、储存文件到s3
        file_key, url = FileStore().store_file_from_user(
            user_id=g.user.id,
            file_obj=file_obj,
            content_type=content_type,
            suffix=file_suffix,
            file_path=file_name,
        )
        if not file_key:
            print(url)
            raise LogicError('保存文件失败')

        obj = HedgeFundCustodianData.filter_by_query(
            manager_id=g.token.manager_id,
            fof_id=fof_id,
            datetime=date,
        ).first()
        obj.url = file_key
        obj.save()

        g.user_operation = '上传托管净值文件'
        g.user_operation_params = {
            'fof_id': fof_id,
            'date': date,
        }
        return


class CusNavFileHtml(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        """解析文件到html格式"""
        file_key = request.args.get('file_key')

        obj = HedgeFundCustodianData.filter_by_query(
            manager_id=g.token.manager_id,
            fof_id=fof_id,
            url=file_key,
        ).one_or_none()
        if not obj:
            return make_response('')

        data = FileStore().load_from_s3(file_key)
        wb = load_workbook(filename=data)
        out = io.StringIO()
        xlsx2html(wb=wb, output=out)
        response = make_response(out.getvalue())
        response.headers["Content-type"] = "text/html"
        return response

    @login_required
    def delete(self, fof_id):
        """删除托管数据和文件"""
        date_str = request.args.get('datetime')
        obj = HedgeFundCustodianData.filter_by_query(
            manager_id=g.token.manager_id,
            fof_id=fof_id,
            datetime=date_str,
        ).first()

        if not obj:
            raise VerifyError('')
        obj.delete()

        g.user_operation = '删除托管净值文件'
        g.user_operation_params = {
            'fof_id': fof_id,
            'date': date_str,
        }
