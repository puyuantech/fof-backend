from flask import Blueprint
from flask_restful import Api
from .view import ProductionsAPI, ProductionAPI, ProductionDetail, ProductionTrades, ProductionPosition

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/production')
api = Api(blu)

api.add_resource(ProductionsAPI, '')
api.add_resource(ProductionAPI, '/<string:_id>')
api.add_resource(ProductionDetail, '/detail/<string:_id>')
api.add_resource(ProductionTrades, '/trades/<string:_id>')
api.add_resource(ProductionPosition, '/cur_position/<string:_id>')


