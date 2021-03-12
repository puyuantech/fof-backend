from flask import request, g
from models import User, ManagerUserMap
from bases.viewhandler import ApiViewHandler
from bases.globals import db
from utils.helper import generate_sql_pagination
from utils.decorators import params_required, super_admin_login_required, login_required
from bases.constants import StuffEnum
from .libs.staff import register_staff_user, update_user_info


class StaffsAPI(ApiViewHandler):

    @super_admin_login_required
    def get(self):
        p = generate_sql_pagination()
        query = db.session.query(User).filter(
            User.is_staff == True,
            User.is_wx == False,
            User.is_deleted == False,
            User.id == ManagerUserMap.user_id,
            ManagerUserMap.manager_id == g.token.manager_id,
        )
        data = p.paginate(query)
        return data

    @super_admin_login_required
    @params_required(*['username', 'password'])
    def post(self):
        # 创建员工
        user = register_staff_user(
            self.input.username,
            self.input.password,
        )

        # 添加用户信息
        update_user_info(user)
        return 'success'


class StaffAPI(ApiViewHandler):

    @super_admin_login_required
    def get(self, _id):
        instance = User.get_by_id(_id)
        return instance.to_dict()

    @super_admin_login_required
    def put(self, _id):
        user = User.get_by_id(_id)
        user = update_user_info(user)
        if self.input.role_id:
            for i in user.token:
                i.delete()
        return user.to_dict()

    @super_admin_login_required
    def delete(self, _id):
        user = User.get_by_id(_id)
        user.logic_delete()


class ResetStaffPassword(ApiViewHandler):

    @super_admin_login_required
    def put(self, _id):
        password = request.json.get('password')
        password = password if password else '123456'
        user = User.get_by_id(_id)
        user.password = password
        user.save()
        return 'success'
