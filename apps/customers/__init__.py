from flask import Blueprint
from flask_restful import Api
from .view import CusAPI, CustomerAPI, CustomerPosition, CustomerTrades, CustomerFile, CustomerTradesSingle,\
    CustomerPositionSingle, CustomerTradesDivCar, CustomerTradesPurRed, CusByFileAPI
from .view_tags import *
from .view_position import PositionAnalysis
from .view_account import SubAccount
from .view_prodictions   import CusProductions

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/customer')
api = Api(blu)

api.add_resource(CusAPI, '')
api.add_resource(CusByFileAPI, '/create_by_file')
api.add_resource(CustomerAPI, '/<int:_id>')
api.add_resource(CustomerPosition, '/position/<string:investor_id>')
api.add_resource(CustomerPositionSingle, '/position_single/<string:investor_id>')
api.add_resource(PositionAnalysis, '/position_analysis/<string:investor_id>')

api.add_resource(CustomerTrades, '/trades/<string:investor_id>')
api.add_resource(CustomerTradesSingle, '/trade_single/<int:trade_id>')
api.add_resource(CustomerTradesPurRed, '/trades_pur_redeem/<string:investor_id>')
api.add_resource(CustomerTradesDivCar, '/trade_dividend_carry/<string:investor_id>')

api.add_resource(CustomerFile, '/download')
api.add_resource(TagAPI, '/tag')
api.add_resource(TagsAPI, '/tag/user')
api.add_resource(TopTagsAPI, '/tag/top')
api.add_resource(SubAccount, '/add_sub_account/<string:investor_id>')
api.add_resource(CusProductions, '/cus_productions/<string:investor_id>')
