import pandas as pd

from flask import request

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from models import FOFInfo, FOFNav, FOFAssetAllocation
from utils.decorators import params_required
from utils.helper import generate_sql_pagination, replace_nan
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
        return data


class ProductionTrades(ApiViewHandler):

    def get(self, _id):
        query = db.session.query(FOFAssetAllocation).filter(
            FOFAssetAllocation.fof_id == _id,
        )
        df = pd.read_sql(query.statement, query.session.bind)
        return replace_nan(df.to_dict(orient='records'))


class ProductionPosition(ApiViewHandler):

    def get(self, _id):
        query = db.session.query(FOFAssetAllocation).filter(
            FOFAssetAllocation.fof_id == _id,
        )
        df = pd.read_sql(query.statement, query.session.bind)
        if len(df) < 1:
            return {}
        data = SurfingCalculator.get_stat_result(df['datetime'], df['nav'])
        return data
