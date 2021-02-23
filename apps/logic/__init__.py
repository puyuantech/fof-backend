from flask import Blueprint
from flask_restful import Api
from .view import LogicAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/logic')
api = Api(blu)

api.add_resource(LogicAPI, '')

