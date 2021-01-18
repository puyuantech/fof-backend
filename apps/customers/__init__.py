from flask import Blueprint
from flask_restful import Api
from .view import CusAPI, CustomerAPI, CustomerPosition, CustomerTrades

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/customer')
api = Api(blu)

api.add_resource(CusAPI, '')
api.add_resource(CustomerAPI, '/<int:_id>')
api.add_resource(CustomerPosition, '/position/<string:investor_id>')
api.add_resource(CustomerTrades, '/trades/<string:investor_id>')

