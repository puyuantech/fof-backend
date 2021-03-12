from flask import Blueprint
from flask_restful import Api
from .view import Logout, Logic, InvestorMobileLoginAPI, ChoseInvestor

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/auth')
api = Api(blu)

# api.add_resource(LoginAPI, '/login')
# api.add_resource(MobileLoginAPI, '/mobile_login')
# api.add_resource(RegisterAPI, '/register')

api.add_resource(Logout, '/logout')
api.add_resource(Logic, '/logic', endpoint='logic')
api.add_resource(InvestorMobileLoginAPI, '/investor_mobile_login')
api.add_resource(ChoseInvestor, '/chose_investor')

