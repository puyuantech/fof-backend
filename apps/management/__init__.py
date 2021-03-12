from flask import Blueprint
from flask_restful import Api

from .view_management import ManagementAPI, ManagementListAPI, ManagementFundAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/management')
api = Api(blu)

api.add_resource(ManagementAPI, '/<string:manager_id>')
api.add_resource(ManagementListAPI, '/list')
api.add_resource(ManagementFundAPI, '/fund/<string:fund_id>')
