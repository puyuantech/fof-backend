from flask import Blueprint
from flask_restful import Api
from .view import OperationsAPI, OperationsListAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/operation')
api = Api(blu)

api.add_resource(OperationsAPI, '')
api.add_resource(OperationsListAPI, '/list')
