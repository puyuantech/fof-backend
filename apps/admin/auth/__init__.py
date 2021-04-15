from flask import Blueprint
from flask_restful import Api
from .view import AdminLoginAPI, ResetAdminPassword

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/admin_auth')
api = Api(blu)

api.add_resource(AdminLoginAPI, '/login')
api.add_resource(ResetAdminPassword, '/change_password')
