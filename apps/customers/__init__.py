from flask import Blueprint
from flask_restful import Api
from .view import CusAPI, CustomerAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/customer')
api = Api(blu)

api.add_resource(CusAPI, '')
api.add_resource(CustomerAPI, '/<int:_id>')

