import pandas as pd
import traceback
import datetime
from flask import request, current_app

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import HedgeFundInfo, HedgeFundNAV, HedgeComment
from utils.decorators import params_required
from utils.helper import generate_sql_pagination, replace_nan

from surfing.util.calculator import Calculator as SurfingCalculator

from .libs import update_hedge_fund_info, make_hedge_fund_info, update_hedge_value


class HedgesAPI(ApiViewHandler):

    def get(self):
        p = generate_sql_pagination()
        query = HedgeFundInfo.filter_by_query()
        data = p.paginate(query, call_back=lambda x: [make_hedge_fund_info(i) for i in x])

        return data

    @params_required(*['fund_id'])
    def post(self):
        data = {
            'fund_id': request.json.get('fund_id'),
            'fund_name': request.json.get('fund_name'),
            'manager_id': request.json.get('manager_id'),
            'water_line': request.json.get('water_line'),
            'incentive_fee_mode': request.json.get('incentive_fee_mode'),
            'incentive_fee_ratio': request.json.get('incentive_fee_ratio'),
            'v_nav_decimals': request.json.get('v_nav_decimals'),
        }
        if HedgeFundInfo.filter_by_query(fund_id=self.input.fund_id).one_or_none():
            raise VerifyError('ID 重复')
        obj = HedgeFundInfo.create(**data)
        update_hedge_fund_info(obj)
        return


class HedgeCommentAPI(ApiViewHandler):

    @params_required(*['comment'])
    def post(self, _id):
        HedgeComment.create(
         fund_id=_id,
         comment=self.input.comment,
        )
        return


class HedgeDetail(ApiViewHandler):

    def get(self, _id):
        query = db.session.query(HedgeFundNAV).filter(
            HedgeFundNAV.fund_id == _id,
        )
        df = pd.read_sql(query.statement, query.session.bind)
        df = df.reset_index()
        if len(df) < 1:
            return {}

        data = {
            'dates': df['datetime'].to_list(),
            'v_net_value': df['v_net_value'].to_list(),
            'net_asset_value': df['v_net_value'].to_list(),
            'acc_unit_value': df['v_net_value'].to_list(),
            'ratios': SurfingCalculator.get_stat_result_from_df(df, 'datetime', 'v_net_value').__dict__,
        }
        return replace_nan(data)


class HedgeAPI(ApiViewHandler):

    def get(self, _id):
        obj = HedgeFundInfo.get_by_query(fund_id=_id)
        data = make_hedge_fund_info(obj)
        return data

    def put(self, _id):
        obj = HedgeFundInfo.get_by_query(fund_id=_id)
        update_hedge_fund_info(obj)
        return

    def delete(self, _id):
        obj = HedgeFundInfo.get_by_query(fund_id=_id)
        obj.logic_delete()

    @params_required(*['method'])
    def post(self, _id):
        obj = HedgeFundInfo.get_by_query(fund_id=_id)

        req_file = request.files.get('file')
        if not req_file:
            raise VerifyError('Couldn\'t find any uploaded file')

        # 解析文件
        try:
            df = pd.read_csv(
                req_file,
                index_col=None,
                dtype={'日期': str, '累计净值': float, '单位净值': float, '虚拟净值': float},
            )
            df = df[['日期', '累计净值', '单位净值', '虚拟净值']]
            df['日期'] = df['日期'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())
            df = df.rename(columns={
                '日期': 'datetime',
                '累计净值': 'acc_unit_value',
                '单位净值': 'net_asset_value',
                '虚拟净值': 'v_net_value',
            })
            df['fund_id'] = _id
            df['insert_time'] = datetime.datetime.now().date()
        except:
            current_app.logger.error(traceback.format_exc())
            raise VerifyError('解析失败')

        # 完全覆盖
        if self.input.method == 'all':
            HedgeFundNAV.filter_by_query(fof_id=_id).delete()
            db.session.execute(
                HedgeFundNAV.__table__.insert(),
                df.to_dict(orient='r'),
            )
            db.session.commit()
            update_hedge_value(_id)
            return 'success'

        # 部分覆盖
        if self.input.method == 'part':
            db.session.query(HedgeFundNAV).filter(
                HedgeFundNAV.fund_id == _id,
                HedgeFundNAV.datetime.in_(df['datetime'].to_list())
            ).delete(synchronize_session=False)
            db.session.execute(
                HedgeFundNAV.__table__.insert(),
                df.to_dict(orient='records'),
            )
            db.session.commit()
            update_hedge_value(_id)
            return 'success'
        raise VerifyError('参数错误')


class HedgeSingleChangeAPI(ApiViewHandler):

    @params_required(*['fund_id', 'datetime', 'net_asset_value', 'acc_unit_value', 'v_net_value'])
    def post(self):
        date = datetime.datetime.strptime(
            self.input.datetime,
            '%Y-%m-%d'
        )
        obj = HedgeFundNAV.filter_by_query(
            fund_id=self.input.fund_id,
            datetime=date,
        ).one_or_none()
        if not obj:
            raise VerifyError('修改目标不存在！')

        obj.net_asset_value = self.input.net_asset_value
        obj.acc_unit_value = self.input.acc_unit_value
        obj.v_net_value = self.input.v_net_value
        obj.save()
        update_hedge_value(self.input.fund_id)
        return

