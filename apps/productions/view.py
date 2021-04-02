import pandas as pd
import json
import time
import datetime
import traceback

from flask import request, current_app, g

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import FOFInfo, FOFNav, FOFNavPublic, FOFAssetAllocation, FOFPosition, FOFInvestorPosition, User, \
    FOFScaleAlteration, UnitMap, WeChatUnionID, UserInvestorMap
from utils.decorators import params_required, login_required, admin_login_required
from utils.helper import generate_sql_pagination, replace_nan, generate_hash_char
from utils.caches import get_fund_collection_caches, get_hedge_fund_cache, get_fund_cache
from surfing.util.calculator import Calculator as SurfingCalculator
from surfing.data.manager.manager_fof import FOFDataManager

from bases.constants import StuffEnum
from .libs import update_production_info, parse_trade_file, create_single_trade, update_trade, parse_nav_file, \
    create_single_nav, update_nav, parse_investor_trade_file
from .mixin import ProMixin


class CreateProductionID(ApiViewHandler):
    @login_required
    def get(self):
        num = int(str(g.user.id) + datetime.datetime.now().strftime('%Y%m%d%H%M%S')[2:])
        _id = generate_hash_char(num)
        return {
            'id': _id,
        }


class ProductionsAPI(ApiViewHandler):

    @login_required
    def get(self):
        manager_id = g.token.manager_id if request.args.get('is_private') else 1

        p = generate_sql_pagination()
        query = FOFInfo.filter_by_query(
            manager_id=manager_id,
        )
        data = p.paginate(
            query,
            equal_filter=[FOFInfo.fof_name, FOFInfo.fof_id, FOFInfo.strategy_type, FOFInfo.is_fof, FOFInfo.fof_status, FOFInfo.asset_type, FOFInfo.is_on_sale],
            range_filter=[FOFInfo.established_date]
        )
        return data

    @login_required
    @params_required(*['fof_id'])
    def post(self):
        manager_id = g.token.manager_id if request.json.get('is_private') else '1'
        data = {
            'fof_id': request.json.get('fof_id'),
            'manager_id': g.token.manager_id if request.json.get('is_private') else '1',
            'datetime':  request.json.get('datetime'),
            'fof_name': request.json.get('fof_name'),
            'admin': request.json.get('admin'),
            'established_date': request.json.get('established_date'),
            'fof_status': request.json.get('fof_status'),
            'subscription_fee': request.json.get('subscription_fee'),
            'redemption_fee': request.json.get('redemption_fee'),
            'management_fee': request.json.get('management_fee'),
            'custodian_fee': request.json.get('custodian_fee'),
            'administrative_fee': request.json.get('administrative_fee'),
            'lock_up_period': request.json.get('lock_up_period'),
            'incentive_fee_mode': request.json.get('incentive_fee_mode'),
            'incentive_fee': request.json.get('incentive_fee'),
            'current_deposit_rate': request.json.get('current_deposit_rate'),
            'initial_raised_fv': request.json.get('initial_raised_fv', 1),
            'initial_net_value': request.json.get('initial_net_value'),
            'incentive_fee_type': request.json.get('incentive_fee_type'),
            'incentive_fee_str': request.json.get('incentive_fee_str'),
            'strategy_type': request.json.get('strategy_type'),
            'risk_type': request.json.get('risk_type'),
            'is_fof': request.json.get('is_fof'),
            'is_on_sale': request.json.get('is_on_sale'),
            'benchmark': request.json.get('benchmark'),
            'asset_type': request.json.get('asset_type'),
            'nav_freq': request.json.get('nav_freq'),
            'fof_manager': request.json.get('fof_manager'),
            'benchmark_index': request.json.get('benchmark_index'),
            'desc_name': request.json.get('desc_name'),
        }
        if FOFInfo.filter_by_query(
            fof_id=self.input.fof_id,
            manager_id=manager_id,
            show_deleted=True
        ).one_or_none():
            raise VerifyError('ID 重复')
        obj = FOFInfo.create(**data)
        return {
            'id': obj.fof_id,
        }


class ProductionAPI(ApiViewHandler, ProMixin):

    @login_required
    def get(self, _id):
        obj = self.select_model(fof_id=_id)
        return obj.to_dict()

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.OPE_MANAGER])
    def put(self, _id):
        obj = self.select_model(fof_id=_id)
        update_production_info(obj)
        return

    @login_required
    def delete(self, _id):
        obj = self.select_model(fof_id=_id)
        obj.logic_delete()


class ProductionNavPublic(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        results = FOFNavPublic.filter_by_query(
            fof_id=fof_id,
        ).all()
        df = pd.DataFrame([i.to_dict() for i in results])
        if len(df) < 1:
            return {}

        data = {
            'dates': df['datetime'].to_list(),
            'nav': df['nav'].to_list(),
            'acc_net_value': df['acc_net_value'].to_list(),
            'volume': df['volume'].to_list(),
            'mv': df['mv'].to_list(),
            'ret': df['ret'].to_list(),
            'ratios': SurfingCalculator.get_stat_result_from_df(df, 'datetime', 'nav').__dict__,
        }
        return replace_nan(data)

    @login_required
    def put(self, fof_id):
        df = parse_nav_file(fof_id)
        db.session.query(
            FOFNavPublic
        ).filter(
            FOFNavPublic.fof_id == fof_id,
            FOFNavPublic.datetime.in_(df['datetime']),
        ).delete(synchronize_session=False)

        for d in df.to_dict(orient='records'):
            new = FOFNavPublic(**replace_nan(d))
            db.session.add(new)
        db.session.commit()

    @login_required
    def delete(self, fof_id):
        FOFNavPublic.filter_by_query(fof_id=fof_id).delete()


class ProductionNavPublicSingle(ApiViewHandler):

    @params_required(*['datetime'])
    @login_required
    def put(self, fof_id):
        date = datetime.datetime.strptime(
            self.input.datetime,
            '%Y-%m-%d',
        ).date()
        obj = FOFNavPublic.filter_by_query(
            fof_id=fof_id,
            datetime=date,
        ).one_or_none()
        if not obj:
            raise VerifyError('不存在！')
        update_nav(obj)

    @params_required(*['datetime'])
    @login_required
    def post(self, fof_id):
        date = datetime.datetime.strptime(
            self.input.datetime,
            '%Y-%m-%d',
        ).date()
        obj = FOFNavPublic.filter_by_query(
            fof_id=fof_id,
            datetime=date,
        ).one_or_none()
        if obj:
            raise VerifyError('此日期数据已存在！')

        FOFNavPublic.create(
            fof_id=fof_id,
            datetime=date,
            nav=request.json.get('nav'),
            acc_net_value=request.json.get('nav'),
            volume=request.json.get('volume'),
            mv=request.json.get('mv'),
            ret=request.json.get('ret'),
        )

    @params_required(*['datetime'])
    @login_required
    def delete(self, fof_id):
        date = datetime.datetime.strptime(
            self.input.datetime,
            '%Y-%m-%d',
        ).date()
        obj = FOFNavPublic.filter_by_query(
            fof_id=fof_id,
            datetime=date,
        ).one_or_none()
        if not obj:
            raise VerifyError('不存在！')
        obj.delete()


class ProductionNav(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        results = FOFNav.filter_by_query(
            fof_id=fof_id,
        ).all()
        df = pd.DataFrame([i.to_dict() for i in results])
        if len(df) < 1:
            return {}

        data = {
            'dates': df['datetime'].to_list(),
            'nav': df['nav'].to_list(),
            'acc_net_value': df['acc_net_value'].to_list(),
            'volume': df['volume'].to_list(),
            'mv': df['mv'].to_list(),
            'ret': df['ret'].to_list(),
            'ratios': SurfingCalculator.get_stat_result_from_df(df, 'datetime', 'nav').__dict__,
        }
        return replace_nan(data)

    @login_required
    def put(self, fof_id):
        df = parse_nav_file(fof_id)
        db.session.query(
            FOFNav
        ).filter(
            FOFNav.fof_id == fof_id,
            FOFNav.datetime.in_(df['datetime']),
        ).delete(synchronize_session=False)

        for d in df.to_dict(orient='records'):
            new = FOFNav(**replace_nan(d))
            db.session.add(new)
        db.session.commit()

    @login_required
    def delete(self, fof_id):
        FOFNav.filter_by_query(fof_id=fof_id).delete()


class ProductionNavSingle(ApiViewHandler):

    @params_required(*['datetime'])
    @login_required
    def put(self, fof_id):
        date = datetime.datetime.strptime(
            self.input.datetime,
            '%Y-%m-%d',
        ).date()
        obj = FOFNav.filter_by_query(
            fof_id=fof_id,
            datetime=date,
        ).one_or_none()
        if not obj:
            raise VerifyError('不存在！')
        update_nav(obj)

    @params_required(*['datetime'])
    @login_required
    def post(self, fof_id):
        date = datetime.datetime.strptime(
            self.input.datetime,
            '%Y-%m-%d',
        ).date()
        obj = FOFNav.filter_by_query(
            fof_id=fof_id,
            datetime=date,
        ).one_or_none()
        if obj:
            raise VerifyError('此日期数据已存在！')
        create_single_nav(fof_id, date)

    @params_required(*['datetime'])
    @login_required
    def delete(self, fof_id):
        date = datetime.datetime.strptime(
            self.input.datetime,
            '%Y-%m-%d',
        ).date()
        obj = FOFNav.filter_by_query(
            fof_id=fof_id,
            datetime=date,
        ).one_or_none()
        if not obj:
            raise VerifyError('不存在！')
        obj.delete()


class ProductionTrades(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        fund_name_dict = get_fund_cache()
        event_type = request.args.get('event_type')

        p = generate_sql_pagination()
        if event_type:
            query = FOFAssetAllocation.filter_by_query(
                fof_id=fof_id,
                event_type=event_type,
            )
        else:
            query = FOFAssetAllocation.filter_by_query(fof_id=fof_id)
        data = p.paginate(query)

        results = data['results']
        for i in results:
            i['fund_name'] = fund_name_dict.get(i['fund_id'])
        return data

    @login_required
    def put(self, fof_id):
        df = parse_trade_file(fof_id)

        for d in df.to_dict(orient='records'):
            new = FOFAssetAllocation(**replace_nan(d))
            db.session.add(new)
        db.session.commit()

    @login_required
    def post(self, fof_id):
        create_single_trade(fof_id)

    @login_required
    def delete(self, fof_id):
        FOFAssetAllocation.filter_by_query(fof_id=fof_id).delete()


class ProductionTradesSingle(ApiViewHandler):

    @login_required
    def put(self, trade_id):
        obj = FOFAssetAllocation.get_by_id(trade_id)
        update_trade(obj)

    @login_required
    def delete(self, trade_id):
        obj = FOFAssetAllocation.get_by_id(trade_id)
        obj.delete()


class ProductionInvestorTrades(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        def fill_trade_info(obj):
            data_dict = obj.to_dict()
            unit_map = UnitMap.filter_by_query(
                investor_id=obj.investor_id,
                manager_id=g.token.manager_id,
                is_deleted=False,
            ).first()

            data_dict['investor_id'] = unit_map.investor_id if unit_map else None
            data_dict['unit_id'] = unit_map.id if unit_map else None
            data_dict['name'] = unit_map.name if unit_map else None
            data_dict['investor_type'] = unit_map.investor_type if unit_map else None
            return data_dict

        p = generate_sql_pagination()
        event_type = request.args.get('event_type')
        if event_type:
            event_type = [int(i) for i in event_type.split(',')]
            query = db.session.query(FOFScaleAlteration).filter(
                FOFScaleAlteration.fof_id == fof_id,
                FOFScaleAlteration.event_type.in_(event_type),
            )
        else:
            query = FOFScaleAlteration.filter_by_query(fof_id=fof_id)
        data = p.paginate(query, call_back=lambda x: [fill_trade_info(i) for i in x])
        return data

    @login_required
    def put(self, fof_id):
        df = parse_investor_trade_file(fof_id=fof_id)

        for d in df.to_dict(orient='records'):
            new = FOFScaleAlteration(**replace_nan(d))
            db.session.add(new)
        db.session.commit()

    @login_required
    def post(self, fof_id):
        try:
            FOFScaleAlteration.create(
                fof_id=fof_id,
                datetime=request.json.get('datetime'),
                investor_id=request.json.get('investor_id'),
                applied_date=request.json.get('applied_date'),
                deposited_date=request.json.get('deposited_date'),
                amount=request.json.get('amount'),
                share=request.json.get('share'),
                nav=request.json.get('nav'),
                status=request.json.get('status'),
                asset_type=request.json.get('asset_type', 2),
                event_type=request.json.get('event_type'),
                manager_id=g.token.manager_id,
            )
        except:
            current_app.logger.error(traceback.format_exc())
            raise VerifyError('创建失败！')

    @login_required
    def delete(self, fof_id):
        FOFScaleAlteration.filter_by_query(fof_id=fof_id).delete()


class ProductionInvestorTradesSingle(ApiViewHandler):

    @login_required
    def put(self, trade_id):
        obj = FOFScaleAlteration.get_by_id(trade_id)
        columns = [
            'datetime',
            'fof_id',
            'investor_id',
            'applied_date',
            'deposited_date',
            'amount',
            'share',
            'nav',
            'status',
            'asset_type',
            'event_type',
        ]
        for i in columns:
            if request.json.get(i) is not None:
                obj.update(commit=False, **{i: request.json.get(i)})
        return

    @login_required
    def delete(self, trade_id):
        obj = FOFScaleAlteration.get_by_id(trade_id)
        obj.delete()


class ProductionInvestor(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.OPE_MANAGER, StuffEnum.FUND_MANAGER])
    def get(self, fof_id):
        investor_return = FOFDataManager.get_investor_return(fof_id)
        if isinstance(investor_return, pd.DataFrame) and len(investor_return) > 1:
            investor_return['shares_sum'] = investor_return['shares'].sum()
            investor_return['shares_weight'] = investor_return['shares'] / investor_return['shares_sum']

        info = FOFInfo.filter_by_query(
            fof_id=fof_id,
            manager_id=g.token.manager_id,
        ).one_or_none()
        if not info:
            raise VerifyError('产品不存在！')

        investor_positions = db.session.query(
            FOFInvestorPosition.investor_id,
            FOFInvestorPosition.shares,
            FOFInvestorPosition.amount,
        ).filter(
            FOFInvestorPosition.fof_id == fof_id,
        ).all()
        investor_ids = [i[0] for i in investor_positions]
        positions = {
            i[0]: {
                'shares': i[1],
                'amount': i[2],
            }
            for i in investor_positions
        }

        unit_maps = db.session.query(UnitMap).filter(
            UnitMap.investor_id.in_(investor_ids),
            UnitMap.manager_id == g.token.manager_id,
        ).all()

        data = []
        for i in unit_maps:
            d = i.to_dict()
            wx = db.session.query(WeChatUnionID).filter(
                UserInvestorMap.investor_id == d['investor_id'],
                UserInvestorMap.map_type == UserInvestorMap.MapType.MAIN,
                UserInvestorMap.user_id == User.id,
                User.id == WeChatUnionID.user_id,
                WeChatUnionID.manager_id == g.token.manager_id,
            ).first()
            if wx:
                d['wx_nick_name'] = wx.nick_name
                d['wx_avatar_url'] = wx.avatar_url
                d['wx_open_id'] = wx.open_id
            d.update({
                'user_amount': positions.get(i.investor_id)['amount'],
                'user_shares': positions.get(i.investor_id)['shares'],
            })
            try:
                d.update({
                    'user_latest_mv': investor_return.loc[i.investor_id, 'latest_mv'],
                    'user_total_rr': investor_return.loc[i.investor_id, 'total_rr'],
                    'user_v_nav': investor_return.loc[i.investor_id, 'v_nav'],
                    'user_shares_weight': investor_return.loc[i.investor_id, 'shares_weight'],
                })
            except Exception:
                current_app.logger.info(traceback.format_exc())
                d.update({
                    'user_total_rr': None,
                    'user_v_nav': None,
                    'user_shares_weight': None,
                })
            data.append(d)

        return replace_nan(data)


class ProductionPosition(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        def helper(x):
            try:
                if x['asset_type'] == '1':
                    x['fund_name'] = mutual_fund.loc[x['fund_id'], 'fund_name']
                    x['order_book_id'] = mutual_fund.loc[x['fund_id'], 'order_book_id']
                if x['asset_type'] == '2':
                    x['fund_name'] = hedge_fund.loc[x['fund_id'], 'fund_name']
                    x['order_book_id'] = hedge_fund.loc[x['fund_id'], 'order_book_id']
            except KeyError:
                pass
            return x

        mutual_fund = get_fund_collection_caches()
        hedge_fund = get_hedge_fund_cache()

        position = db.session.query(FOFPosition).filter(
            FOFPosition.fof_id == fof_id,
        ).order_by(FOFPosition.datetime.desc()).limit(1).first()
        if not position:
            return []
        df = pd.DataFrame(json.loads(position.position))
        if len(df) < 1:
            return []
        df['datetime'] = position.datetime
        df['total_current'] = position.total_current if position.total_current else 0
        df['asset_type'] = df['asset_type'].astype(str)
        df['amount'] = df['share'] * df['nav']
        df['sum_amount'] = df['amount'].sum() + df['total_current']
        df['weight'] = df['amount'] / df['sum_amount']
        df = df.apply(helper, axis=1)
        return replace_nan(df.to_dict(orient='records'))
