from flask import Blueprint
from flask_restful import Api
from .view import WX, WXBindUser

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/wx')
api = Api(blu)

api.add_resource(WX, '')
api.add_resource(WXBindUser, '/user')

