from flask import Blueprint
from flask_restful import Api
from .view import IndexSearcherAPI, IndexPointAPI, IndexMonthlyRetAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/index')
api = Api(blu)

api.add_resource(IndexSearcherAPI, '/searcher/<string:key_word>')
api.add_resource(IndexPointAPI, '/point/<string:index_id>')
api.add_resource(IndexMonthlyRetAPI, '/monthly_ret/<string:index_id>')
