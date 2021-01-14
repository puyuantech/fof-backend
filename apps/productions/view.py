import pandas as pd
import json

from flask import request

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import FOFInfo, FOFNav, FOFAssetAllocation, FOFPosition
from utils.decorators import params_required
from utils.helper import generate_sql_pagination, replace_nan
from utils.caches import get_fund_collection_caches, get_hedge_fund_cache
from surfing.util.calculator import Calculator as SurfingCalculator

from .libs import update_production_info


class ProductionsAPI(ApiViewHandler):
    def get(self):
        p = generate_sql_pagination()
        query = FOFInfo.filter_by_query()
        data = p.paginate(query)
        return data

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

    def get(self, _id):
        obj = FOFInfo.get_by_query(fof_id=_id)
        return obj.to_dict()

    def put(self, _id):
        obj = FOFInfo.get_by_query(fof_id=_id)
        update_production_info(obj)
        return

    def delete(self, _id):
        obj = FOFInfo.get_by_query(fof_id=_id)
        obj.logic_delete()


class ProductionDetail(ApiViewHandler):

    def get(self, _id):
        query = db.session.query(FOFNav).filter(
            FOFNav.fof_id == _id,
        )
        df = pd.read_sql(query.statement, query.session.bind)
        if len(df) < 1:
            return {}

        data = {
            'dates': df['datetime'].to_list(),
            'values': df['nav'].to_list(),
            'ratios': SurfingCalculator.get_stat_result_from_df(df, 'datetime', 'nav').__dict__,
        }
        return replace_nan(data)


class ProductionTrades(ApiViewHandler):

    def get(self, _id):
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

        query = db.session.query(FOFAssetAllocation).filter(
            FOFAssetAllocation.fof_id == _id,
        )
        df = pd.read_sql(query.statement, query.session.bind)
        df = df.apply(helper, axis=1)
        return replace_nan(df.to_dict(orient='records'))


class ProductionPosition(ApiViewHandler):

    def get(self, _id):
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
            FOFPosition.fof_id == _id,
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
