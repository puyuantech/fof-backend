from flask import Blueprint
from flask_restful import Api
from .view import WX, OfficeAPPID, WxLoginAPI, WXBindMobile

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/wx')
api = Api(blu)

api.add_resource(WX, '/trans/<string:manager_id>')
api.add_resource(WxLoginAPI, '/official_login/<string:manager_id>')
api.add_resource(WXBindMobile, '/bind_mobile')
api.add_resource(OfficeAPPID, '/office_app_id')

