from flask import Blueprint
from flask_restful import Api
from .view import AdminLoginAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/manager_wx')
api = Api(blu)

api.add_resource(AdminLoginAPI, '/<string:manager_id>')
