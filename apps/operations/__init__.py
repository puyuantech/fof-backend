from flask import Blueprint
from flask_restful import Api
from .view import OperationsAPI, OperationsListAPI, InvestorOperationAPI, InvestorOperationsListAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/operation')
api = Api(blu)

api.add_resource(OperationsAPI, '')
api.add_resource(OperationsListAPI, '/list')
api.add_resource(InvestorOperationAPI, '/investor')
api.add_resource(InvestorOperationsListAPI, '/investor/list_action')
