from flask import Blueprint
from flask_restful import Api
from .view import *

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/information')
api = Api(blu)

api.add_resource(InformationAPI, '/info')
api.add_resource(InformationDetailAPI, '/info/<int:_id>')

api.add_resource(TemplateAPI, '/template')
api.add_resource(TemplateDetailAPI, '/template/<int:_id>')
