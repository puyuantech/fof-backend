from flask import Blueprint
from flask_restful import Api
from .view import ResetPassword, ChangeAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/accounts')
api = Api(blu)

api.add_resource(ResetPassword, '/reset_password')
api.add_resource(ChangeAPI, '/change')

