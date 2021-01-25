from flask import Blueprint
from flask_restful import Api
from .view import ProductionsAPI, ProductionAPI, ProductionDetail, ProductionTrades, ProductionPosition, \
    ProductionInvestor, ProductionTradesSingle

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/production')
api = Api(blu)

api.add_resource(ProductionsAPI, '')
api.add_resource(ProductionAPI, '/<string:_id>')
api.add_resource(ProductionDetail, '/detail/<string:fof_id>')
api.add_resource(ProductionTrades, '/trades/<string:fof_id>')
api.add_resource(ProductionTradesSingle, '/trade_single/<int:trade_id>')
api.add_resource(ProductionPosition, '/cur_position/<string:fof_id>')
api.add_resource(ProductionInvestor, '/cur_investors/<string:fof_id>')

