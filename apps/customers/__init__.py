from flask import Blueprint
from flask_restful import Api
from .view import StaffAPI, StaffsAPI, ResetStaffPassword

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/customer')
api = Api(blu)

api.add_resource(StaffsAPI, '')
api.add_resource(StaffAPI, '/<int:_id>')
api.add_resource(ResetStaffPassword, '/reset_pwd/<int:_id>')

