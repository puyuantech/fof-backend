from flask import Blueprint
from flask_restful import Api

from .view_certification import CertificationTokenAPI, CertificationListAPI
from .view_contract import ContractListAPI
from .view_logo import LogoAPI, FOFLogoAPI, FOFLogoListAPI
from .view_notification import NotificationAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/manager')
api = Api(blu)

api.add_resource(CertificationTokenAPI, '/certification/token')
api.add_resource(CertificationListAPI, '/certification/list')

api.add_resource(ContractListAPI, '/contract/list')

api.add_resource(LogoAPI, '/logo')
api.add_resource(FOFLogoAPI, '/fof/logo')
api.add_resource(FOFLogoListAPI, '/fof/logo/list')

api.add_resource(NotificationAPI, '/notification')
