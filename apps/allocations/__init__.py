from flask import Blueprint
from flask_restful import Api
from .views import AllocationAPI, AllocationStatusAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/allocation')
api = Api(blu)

api.add_resource(AllocationAPI, '')
api.add_resource(AllocationStatusAPI, '/status')


