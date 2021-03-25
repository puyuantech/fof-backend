from flask import Blueprint
from flask_restful import Api
from .view import *

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/manager_mail')
api = Api(blu)

api.add_resource(MailVerifyAPI, '/verify')
api.add_resource(MailSettingAPI, '/setting')
