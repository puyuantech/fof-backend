from flask import Blueprint
from flask_restful import Api
from .view import *

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/uploads')
api = Api(blu)

api.add_resource(UploadPDFAPI, '/pdf')
api.add_resource(UploadImageAPI, '/image')
api.add_resource(ParsePDFAPI, '/parse')
api.add_resource(UploadPublicFileAPI, '/public_file')
api.add_resource(UploadPrivateFileAPI, '/private_file')
api.add_resource(ApplyUploadPrivateFileAPI, '/apply_private_file')
api.add_resource(ApplyParseFileKey, '/apply_parse_file_key')
