from bases.viewhandler import ApiViewHandler
from models import FOFAccountStatement, FOFTransitMoney, FOFEstimateFee, FOFEstimateInterest, FOFOtherRecord
from .mixin import ViewDetailMixin, ViewAllMixin
from .libs import update_account_statement, update_transit_money, update_estimate_fee, update_estimate_interest, \
    update_other_record, parse_account_statement, parse_transit_money


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

