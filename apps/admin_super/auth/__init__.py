from flask import Blueprint
from flask_restful import Api
from .view import SuperAdminLoginAPI, Logout, FileParseAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/super/auth')
api = Api(blu)

api.add_resource(SuperAdminLoginAPI, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(FileParseAPI, '/file_parse')
