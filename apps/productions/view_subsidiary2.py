from bases.viewhandler import ApiViewHandler
from models import FOFRealAccountStatement, FOFRealTransitMoney, FOFRealEstimateFee, FOFRealEstimateInterest
from .mixin import ViewDetailMixin, ViewAllMixin
from .libs import update_account_statement, update_transit_money, update_estimate_fee, update_estimate_interest, \
    parse_account_statement, parse_transit_money


class RealAccountStatementAPI(ApiViewHandler, ViewAllMixin):
    model = FOFRealAccountStatement
    update_func = update_account_statement
    parse_func = parse_account_statement


class RealAccountStatementDetailAPI(ApiViewHandler, ViewDetailMixin):
    model = FOFRealAccountStatement
    update_func = update_account_statement


class RealTransitMoneyAPI(ApiViewHandler, ViewAllMixin):
    model = FOFRealTransitMoney
    update_func = update_transit_money
    parse_func = parse_transit_money


class RealTransitMoneyDetailAPI(ApiViewHandler, ViewDetailMixin):
    model = FOFRealTransitMoney
    update_func = update_transit_money


class RealEstimateFeeAPI(ApiViewHandler, ViewAllMixin):
    model = FOFRealEstimateFee
    update_func = update_estimate_fee


class RealEstimateFeeDetailAPI(ApiViewHandler, ViewDetailMixin):
    model = FOFRealEstimateFee
    update_func = update_estimate_fee


class RealEstimateInterestAPI(ApiViewHandler, ViewAllMixin):
    model = FOFRealEstimateInterest
    update_func = update_estimate_interest


class RealEstimateInterestDetailAPI(ApiViewHandler, ViewDetailMixin):
    model = FOFRealEstimateInterest
    update_func = update_estimate_interest

