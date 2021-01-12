from flask import Blueprint
from flask_restful import Api
from .views import StaffAPI, StaffsAPI, ResetStaffPassword

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/')
api = Api(blu)

api.add_resource(StaffsAPI, '/staffs')
api.add_resource(StaffAPI, '/staff/<int:_id>')
api.add_resource(ResetStaffPassword, '/staff/reset_pwd/<int:_id>')

