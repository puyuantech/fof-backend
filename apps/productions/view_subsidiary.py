from flask import request, g

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan, generate_sql_pagination
from models import FOFAccountStatement, FOFTransitMoney, FOFEstimateFee, FOFEstimateInterest, FOFOtherRecord, \
    FOFIncidentalStatement, FOFNavCalc, FOFAssetCorrect
from .mixin import ViewDetailMixin, ViewAllMixin
from .libs import update_account_statement, update_transit_money, update_estimate_fee, update_estimate_interest, \
    update_other_record, parse_account_statement, parse_transit_money, update_incidental_statement


class NavCalcAPI(ApiViewHandler, ViewAllMixin):
    model = FOFNavCalc


def update_fof_asset_correct(self, obj):
    columns = [
        'date',
        'amount',
        'remark',
    ]

    for i in columns:
        if request.json.get(i) is not None:
            obj.update(commit=False, **{i: request.json.get(i)})
    obj.save()
    return obj


class AssetCorrectAPI(ApiViewHandler):
    model = FOFAssetCorrect
    update_func = update_fof_asset_correct

    @login_required
    def get(self, fof_id):
        p = generate_sql_pagination()

        query = self.model.filter_by_query(
            fof_id=fof_id,
            manager_id=g.token.manager_id,
        )
        data = p.paginate(query)
        return data

    @login_required
    def post(self, fof_id):
        obj = self.model(
            manager_id=g.token.manager_id,
            fof_id=fof_id,
        )
        self.update_func(obj)

    @login_required
    def delete(self, fof_id):
        self.model.filter_by_query(
            fof_id=fof_id,
            manager_id=g.token.manager_id,
        ).delete()


class AssetCorrectDetailAPI(ApiViewHandler, ViewDetailMixin):
    model = FOFAssetCorrect
    update_func = update_fof_asset_correct


class AccountStatementAPI(ApiViewHandler, ViewAllMixin):
    model = FOFAccountStatement
    update_func = update_account_statement
    parse_func = parse_account_statement


class AccountStatementDetailAPI(ApiViewHandler, ViewDetailMixin):
    model = FOFAccountStatement
    update_func = update_account_statement


class TransitMoneyAPI(ApiViewHandler, ViewAllMixin):
    model = FOFTransitMoney
    update_func = update_transit_money
    parse_func = parse_transit_money


class TransitMoneyDetailAPI(ApiViewHandler, ViewDetailMixin):
    model = FOFTransitMoney
    update_func = update_transit_money


class EstimateFeeAPI(ApiViewHandler, ViewAllMixin):
    model = FOFEstimateFee
    update_func = update_estimate_fee


class EstimateFeeDetailAPI(ApiViewHandler, ViewDetailMixin):
    model = FOFEstimateFee
    update_func = update_estimate_fee


class EstimateInterestAPI(ApiViewHandler, ViewAllMixin):
    model = FOFEstimateInterest
    update_func = update_estimate_interest


class EstimateInterestDetailAPI(ApiViewHandler, ViewDetailMixin):
    model = FOFEstimateInterest
    update_func = update_estimate_interest


class OtherRecordAPI(ApiViewHandler, ViewAllMixin):
    model = FOFOtherRecord
    update_func = update_other_record


class OtherRecordDetailAPI(ApiViewHandler, ViewDetailMixin):
    model = FOFOtherRecord
    update_func = update_other_record


class IncidentalStatement(ApiViewHandler, ViewAllMixin):
    model = FOFIncidentalStatement
    update_func = update_incidental_statement


class IncidentalStatementDetail(ApiViewHandler, ViewDetailMixin):
    model = FOFIncidentalStatement
    update_func = update_incidental_statement

