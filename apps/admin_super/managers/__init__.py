from flask import Blueprint
from flask_restful import Api
from .view import ManagersAPI, ManagerAPI, SignApplyFileAPI, SignApplyFilesAPI, SignApplyAPI, SignStatusAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/super/manager')
api = Api(blu)

api.add_resource(ManagersAPI, '')
api.add_resource(ManagerAPI, '/detail/<string:_id>')
api.add_resource(SignApplyFileAPI, '/apply_file/<int:_id>')
api.add_resource(SignApplyFilesAPI, '/apply_files')
api.add_resource(SignStatusAPI, '/sign_status/<int:_id>')
api.add_resource(SignApplyAPI, '/sign_apply/<int:_id>')
