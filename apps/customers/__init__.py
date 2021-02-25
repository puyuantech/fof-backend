from flask import Blueprint
from flask_restful import Api
from .view import CusAPI, CustomerAPI, CustomerPosition, CustomerTrades, CustomerFile, CustomerTradesSingle
from .view_tags import *

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/customer')
api = Api(blu)

api.add_resource(CusAPI, '')
api.add_resource(CustomerAPI, '/<int:_id>')
api.add_resource(CustomerPosition, '/position/<string:investor_id>')
api.add_resource(CustomerTrades, '/trades/<string:investor_id>')
api.add_resource(CustomerTradesSingle, '/trade_single/<int:trade_id>')
api.add_resource(CustomerFile, '/download')
api.add_resource(TagAPI, '/tag')
api.add_resource(TagsAPI, '/tag/user')
api.add_resource(TopTagsAPI, '/tag/top')


