from flask import Blueprint
from flask_restful import Api
from .view import HedgesAPI, HedgeAPI, HedgeCommentAPI, HedgeDetail, HedgeSingleChangeAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/hedge')
api = Api(blu)

api.add_resource(HedgesAPI, '')
api.add_resource(HedgeAPI, '/<string:_id>')
api.add_resource(HedgeDetail, '/detail/<string:_id>')
api.add_resource(HedgeCommentAPI, '/comment/<string:_id>')
api.add_resource(HedgeSingleChangeAPI, '/single_change')
