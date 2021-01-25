import pandas as pd
import json

from flask import request

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import FOFInfo, FOFNav, FOFAssetAllocation, FOFPosition, FOFInvestorPosition, User
from utils.decorators import params_required, login_required, admin_login_required
from utils.helper import generate_sql_pagination, replace_nan
from utils.caches import get_fund_collection_caches, get_hedge_fund_cache
from surfing.util.calculator import Calculator as SurfingCalculator

from bases.constants import StuffEnum
from .libs import update_production_info, parse_trade_file, create_single_trade, update_trade


class ProductionsAPI(ApiViewHandler):

    @login_required
    def get(self):
        p = generate_sql_pagination()
        query = FOFInfo.filter_by_query()
        data = p.paginate(query)
        return data

    @login_required
    @params_required(*['fof_id'])
    def post(self):
        data = {
            'fof_id': request.json.get('fof_id'),
            'datetime': request.json.get('datetime'),
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
        }
        if FOFInfo.filter_by_query(fof_id=self.input.fof_id).one_or_none():
            raise VerifyError('ID 重复')
        FOFInfo.create(**data)
        return


class ProductionAPI(ApiViewHandler):

    @login_required
    def get(self, _id):
        obj = FOFInfo.get_by_query(fof_id=_id)
        return obj.to_dict()

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.OPE_MANAGER])
    def put(self, _id):
        obj = FOFInfo.get_by_query(fof_id=_id)
        update_production_info(obj)
        return

    @login_required
    def delete(self, _id):
        obj = FOFInfo.get_by_query(fof_id=_id)
        obj.logic_delete()


class ProductionDetail(ApiViewHandler):

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
            'values': df['nav'].to_list(),
            'ratios': SurfingCalculator.get_stat_result_from_df(df, 'datetime', 'nav').__dict__,
        }
        return replace_nan(data)


class ProductionTrades(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        def helper(x):
            if x['asset_type'] == 1:
                x['fund_name'] = mutual_fund.loc[x['fund_id'], 'fund_name']
                x['order_book_id'] = mutual_fund.loc[x['fund_id'], 'order_book_id']
            if x['asset_type'] == 2:
                x['fund_name'] = hedge_fund.loc[x['fund_id'], 'fund_name']
                x['order_book_id'] = hedge_fund.loc[x['fund_id'], 'order_book_id']
            return x

        mutual_fund = get_fund_collection_caches()
        hedge_fund = get_hedge_fund_cache()

        results = db.session.query(FOFAssetAllocation).filter(
            FOFAssetAllocation.fof_id == fof_id,
        ).all()
        df = pd.DataFrame([i.to_dict() for i in results])
        df = df.apply(helper, axis=1)
        return replace_nan(df.to_dict(orient='records'))

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


class ProductionInvestor(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.OPE_MANAGER, StuffEnum.FUND_MANAGER])
    def get(self, fof_id):
        investor_ids = db.session.query(
            FOFInvestorPosition.investor_id
        ).filter(
            FOFInvestorPosition.fof_id == fof_id,
        ).all()
        investor_ids = [i[0] for i in investor_ids]

        users = db.session.query(User).filter(
            User.investor_id.in_(investor_ids),
        ).all()
        data = [i.to_cus_dict() for i in users]
        return replace_nan(data)


class ProductionPosition(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        def helper(x):
            if x['asset_type'] == '1':
                x['fund_name'] = mutual_fund.loc[x['fund_id'], 'fund_name']
                x['order_book_id'] = mutual_fund.loc[x['fund_id'], 'order_book_id']
            if x['asset_type'] == '2':
                x['fund_name'] = hedge_fund.loc[x['fund_id'], 'fund_name']
                x['order_book_id'] = hedge_fund.loc[x['fund_id'], 'order_book_id']
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
        df['asset_type'] = df['asset_type'].astype(str)
        df['amount'] = df['share'] * df['nav']
        df['sum_amount'] = df['amount'].sum()
        df['weight'] = df['amount'] / df['sum_amount']
        df = df.apply(helper, axis=1)
        return replace_nan(df.to_dict(orient='records'))
