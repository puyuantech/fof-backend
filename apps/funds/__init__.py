from flask import Blueprint
from flask_restful import Api
from .view_searcher import FundSearcherAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/funds')
api = Api(blu)

api.add_resource(FundSearcherAPI, '/searcher/<string:key_word>')
