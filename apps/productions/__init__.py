from flask import Blueprint
from flask_restful import Api
from .view import ProductionsAPI, ProductionAPI, ProductionNav, \
    ProductionNavPublic, ProductionNavPublicSingle, ProductionNavSingle,\
    ProductionTrades, ProductionPosition, \
    ProductionInvestor, ProductionTradesSingle, \
    ProductionInvestorTrades, ProductionInvestorTradesSingle, CreateProductionID
from .view_subsidiary import *
from .view_subsidiary2 import *
from .view_refresh import ProductionRefresh, ProductionPublicRefresh
from .view_profit import ProductionRet, ProductionMonthlyRet, ProductionWinRate, ProductionRatio
from .view_ratios import *
from .view_trades import *
from .view_nav import *
from .view_tags import ProTagAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/production')
api = Api(blu)

api.add_resource(ProductionsAPI, '')
api.add_resource(ProductionAPI, '/<string:_id>')
api.add_resource(CreateProductionID, '/create_id')

api.add_resource(ProductionNavPublic, '/display/<string:fof_id>')
api.add_resource(ProductionNavPublicSingle, '/display_single/<string:fof_id>')

api.add_resource(ProductionNav, '/detail/<string:fof_id>')
api.add_resource(ProductionNavSingle, '/detail_single/<string:fof_id>')

api.add_resource(ProductionTrades, '/trades/<string:fof_id>')
api.add_resource(ProductionTradesSingle, '/trade_single/<int:trade_id>')
api.add_resource(ProductionInvestorTrades, '/investor_trades/<string:fof_id>')
api.add_resource(ProductionInvestorTradesSingle, '/investor_trade_single/<int:trade_id>')
api.add_resource(ProductionPosition, '/cur_position/<string:fof_id>')
api.add_resource(ProductionInvestor, '/cur_investors/<string:fof_id>')

api.add_resource(NavCalcAPI, '/nav_calc/<string:fof_id>')
api.add_resource(AccountStatementAPI, '/account_statement/<string:fof_id>')
api.add_resource(AccountStatementDetailAPI, '/account_statement/detail/<int:_id>')
api.add_resource(EstimateFeeAPI, '/estimate_fee/<string:fof_id>')
api.add_resource(EstimateFeeDetailAPI, '/estimate_fee/detail/<int:_id>')
api.add_resource(EstimateInterestAPI, '/estimate_interest/<string:fof_id>')
api.add_resource(EstimateInterestDetailAPI, '/estimate_interest/detail/<int:_id>')
api.add_resource(TransitMoneyAPI, '/transit_money/<string:fof_id>')
api.add_resource(TransitMoneyDetailAPI, '/transit_money/detail/<int:_id>')
api.add_resource(OtherRecordAPI, '/other_record/<string:fof_id>')
api.add_resource(OtherRecordDetailAPI, '/other_record/detail/<int:_id>')
api.add_resource(IncidentalStatement, '/incidental_statement/<string:fof_id>')
api.add_resource(IncidentalStatementDetail, '/incidental_statement/detail/<int:_id>')

api.add_resource(RealAccountStatementAPI, '/real_account_statement/<string:fof_id>')
api.add_resource(RealAccountStatementDetailAPI, '/real_account_statement/detail/<int:_id>')
api.add_resource(RealEstimateFeeAPI, '/real_estimate_fee/<string:fof_id>')
api.add_resource(RealEstimateFeeDetailAPI, '/real_estimate_fee/detail/<int:_id>')
api.add_resource(RealEstimateInterestAPI, '/real_estimate_interest/<string:fof_id>')
api.add_resource(RealEstimateInterestDetailAPI, '/real_estimate_interest/detail/<int:_id>')
api.add_resource(RealTransitMoneyAPI, '/real_transit_money/<string:fof_id>')
api.add_resource(RealTransitMoneyDetailAPI, '/real_transit_money/detail/<int:_id>')

# profit
api.add_resource(ProductionRet, '/ret/<string:fof_id>')
api.add_resource(ProductionMonthlyRet, '/monthly_ret/<string:fof_id>')
api.add_resource(ProductionWinRate, '/win_rate/<string:fof_id>')
api.add_resource(ProductionRatio, '/ratios/<string:fof_id>')

# refresh
api.add_resource(
    ProductionRefresh,
    '/refresh/<string:fof_id>'
)
api.add_resource(
    ProductionPublicRefresh,
    '/pub_refresh/<string:fof_id>'
)

# ratios
api.add_resource(ProInfoAPI, '/ratios/info/<string:fof_id>')
api.add_resource(ProManagementAPI, '/ratios/management/<string:fof_id>')
api.add_resource(ProNavAPI, '/ratios/nav/<string:fof_id>')
api.add_resource(ProMonthlyRetAPI, '/ratios/monthly_ret/<string:fof_id>')
api.add_resource(ProPeriodRetAPI, '/ratios/period_ret/<string:fof_id>')
api.add_resource(ProRatioAPI, '/ratios/ratio/<string:fof_id>')
api.add_resource(ProRollingProfitAPI, '/ratios/rolling_profit/<string:fof_id>')
api.add_resource(ProDrawDownWaterAPI, '/ratios/mdd_water/<string:fof_id>')

# investor trades
api.add_resource(TradesPurRedeemAPI, '/trades/pur_redeem')
api.add_resource(TradesDivAndCarryAPI, '/trades/dividend')
api.add_resource(TradesCarryEventAPI, '/trades/carry_event')
api.add_resource(TradesDividendEventAPI, '/trades/dividend_event')

# manage nav
api.add_resource(NavTemplateFile, '/manage_nav/template_file')
api.add_resource(NavParseFile, '/manage_nav/parse')
api.add_resource(NavUpdateAPI, '/manage_nav/update/<string:fof_id>')
api.add_resource(NavByDateAPI, '/manage_nav/by_date/<string:fof_id>')

# tags
api.add_resource(ProTagAPI, '/manage_tag')

