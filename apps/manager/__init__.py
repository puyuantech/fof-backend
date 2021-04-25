from flask import Blueprint
from flask_restful import Api

from .view_certification import CertificationTokenAPI, CertificationListAPI
from .view_content import ContentListAPI
from .view_contract import ContractListAPI, FOFListAPI, FOFStartAPI, FOFTemplatesAPI
from .view_customer import CustomerListAPI, CustomerNotificationAPI
from .view_logo import LogoAPI, FOFLogoAPI, FOFLogoListAPI
from .view_notification import NotificationAPI, NotificationStatisticsAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/manager')
api = Api(blu)

api.add_resource(CertificationTokenAPI, '/certification/token')
api.add_resource(CertificationListAPI, '/certification/list')

api.add_resource(ContentListAPI, '/content/list')

api.add_resource(ContractListAPI, '/contract/list')
api.add_resource(FOFListAPI, '/contract/fofs')
api.add_resource(FOFStartAPI, '/contract/fof/start')
api.add_resource(FOFTemplatesAPI, '/contract/fof/templates')

api.add_resource(CustomerListAPI, '/customer/list')
api.add_resource(CustomerNotificationAPI, '/customer/notification')

api.add_resource(LogoAPI, '/logo')
api.add_resource(FOFLogoAPI, '/fof/logo')
api.add_resource(FOFLogoListAPI, '/fof/logo/list')

api.add_resource(NotificationAPI, '/notification')
api.add_resource(NotificationStatisticsAPI, '/notification/statistics')
