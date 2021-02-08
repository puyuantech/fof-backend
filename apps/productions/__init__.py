from flask import Blueprint
from flask_restful import Api
from .view import ProductionsAPI, ProductionAPI, ProductionNav, \
    ProductionNavPublic, ProductionNavSingle,\
    ProductionTrades, ProductionPosition, \
    ProductionInvestor, ProductionTradesSingle
from .view_subsidiary import *

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/production')
api = Api(blu)

api.add_resource(ProductionsAPI, '')
api.add_resource(ProductionAPI, '/<string:_id>')
api.add_resource(ProductionNavPublic, '/display/<string:fof_id>')
api.add_resource(ProductionNav, '/detail/<string:fof_id>')
api.add_resource(ProductionNavSingle, '/detail_single/<string:fof_id>')
api.add_resource(ProductionTrades, '/trades/<string:fof_id>')
api.add_resource(ProductionTradesSingle, '/trade_single/<int:trade_id>')
api.add_resource(ProductionPosition, '/cur_position/<string:fof_id>')
api.add_resource(ProductionInvestor, '/cur_investors/<string:fof_id>')
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

