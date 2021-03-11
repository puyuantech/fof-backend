from flask import Blueprint
from flask_restful import Api
from .view import ManagersAPI, ManagerAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/super/manager')
api = Api(blu)

api.add_resource(ManagersAPI, '')
api.add_resource(ManagerAPI, '/detail/<string:_id>')
