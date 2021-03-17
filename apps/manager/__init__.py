from flask import Blueprint
from flask_restful import Api

from .view_certification import CertificationTokenAPI, CertificationListAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/manager')
api = Api(blu)

api.add_resource(CertificationTokenAPI, '/certification/token')
api.add_resource(CertificationListAPI, '/certification/list')
