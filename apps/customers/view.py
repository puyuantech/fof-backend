from flask import request, g
from models import User, UserLogin
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from bases.constants import StuffEnum
from utils.helper import generate_sql_pagination
from utils.decorators import params_required, super_admin_login_required, admin_login_required
from .libs import get_all_user_info_by_user, register_investor_user, update_user_info


class CusAPI(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def get(self):
        p = generate_sql_pagination()
        query = User.filter_by_query(role_id=StuffEnum.INVESTOR)
        data = p.paginate(query, call_back=lambda x: [get_all_user_info_by_user(i) for i in x])
        return data

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    @params_required(*['mobile'])
    def post(self):
        if not self.is_valid_mobile(self.input.mobile):
            raise VerifyError('电话号码有误！')

        # 创建投资者
        user, user_login = register_investor_user(
            self.input.mobile,
        )

        # 添加信息
        update_user_info(user)
        return 'success'


class CustomerAPI(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def get(self, _id):
        instance = User.filter_by_query(id=_id, role_id=StuffEnum.INVESTOR).first()
        if not instance:
            raise VerifyError('不存在！')
        return get_all_user_info_by_user(instance)

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def put(self, _id):
        instance = User.filter_by_query(id=_id, role_id=StuffEnum.INVESTOR).first()
        if not instance:
            raise VerifyError('不存在！')
        user = update_user_info(instance)
        return get_all_user_info_by_user(user)

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def delete(self, _id):
        user = User.filter_by_query(id=_id, role_id=StuffEnum.INVESTOR).first()
        if not user:
            raise VerifyError('不存在！')
        user_login = UserLogin.filter_by_query(user_id=user.id).first()
        user.logic_delete()
        if user_login:
            user_login.logic_delete()


class ResetStaffPassword(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def put(self, _id):
        password = request.json.get('password')
        password = password if password else '123456'
        user = User.filter_by_query(id=_id, role_id=StuffEnum.INVESTOR).first()
        if not user:
            raise VerifyError('不存在！')

        user_login = UserLogin.filter_by_query(user_id=user.id).one()
        user_login.password = password
        user_login.save()
        return 'success'


