from flask import Blueprint
from flask_restful import Api
from .view import LoginAPI, RegisterAPI, Logout, Logic, MobileLoginAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/auth')
api = Api(blu)

api.add_resource(LoginAPI, '/login')
api.add_resource(MobileLoginAPI, '/mobile_login')
api.add_resource(Logout, '/logout')
# api.add_resource(RegisterAPI, '/register')
api.add_resource(Logic, '/logic')

