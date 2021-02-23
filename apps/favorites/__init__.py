from flask import Blueprint
from flask_restful import Api
from .views import FavoriteAPI, FavoriteDetailAPI, FavoriteStatusAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/favorite')
api = Api(blu)

api.add_resource(FavoriteAPI, '')
api.add_resource(FavoriteDetailAPI, '/<int:_id>')
api.add_resource(FavoriteStatusAPI, '/status')

