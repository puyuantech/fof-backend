from flask import Blueprint
from flask_restful import Api
from .view import *

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/super/apply')
api = Api(blu)

api.add_resource(AppliesAPI, '')
api.add_resource(AppliesCheckEmailAPI, '/check_email')

