from flask import Blueprint
from flask_restful import Api
from .view import WeChatSettingAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/manager_basic')
api = Api(blu)

api.add_resource(WeChatSettingAPI, '/<string:manager_id>')
