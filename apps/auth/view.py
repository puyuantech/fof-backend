from flask import g, request, current_app
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from bases.constants import StuffEnum
from bases.globals import db
from models import Token, User, UserInvestorMap, InvestorInfo, ManagerUserMap, ManagerInfo
from utils.decorators import params_required, login_required
from apps.captchas.libs import check_img_captcha, check_sms_captcha
from .libs import *


# class LoginAPI(ApiViewHandler):
#     @params_required(*['username', 'password', 'verification_code', 'verification_key'])
#     def post(self):
#         g.user_operation = '登录-密码'
#         check_img_captcha(
#             verification_code=self.input.verification_code,
#             verification_key=self.input.verification_key,
#         )
#         user_login = check_login(
#             username=self.input.username,
#             password=self.input.password,
#         )
#         user_dict = get_all_user_info(user_login)
#         user = User.get_by_id(user_login.user_id)
#         token_dict = Token.generate_token(user_login.user_id)
#
#         data = {
#             'user': user_dict,
#             'token': token_dict,
#         }
#         g.user = user
#         return data


# class MobileLoginAPI(ApiViewHandler):
#     @params_required(*['mobile', 'code'])
#     def post(self):
#         g.user_operation = '登录-手机号'
#         check_sms_captcha(
#             verification_code=self.input.code,
#             verification_key=self.input.mobile,
#         )
#         user = get_user_by_mobile(mobile=self.input.mobile)
#         if not user:
#             raise VerifyError('用户不存在')
#         if user.role_id not in [StuffEnum.ADMIN, StuffEnum.OPE_MANAGER, StuffEnum.FUND_MANAGER]:
#             raise VerifyError('权限错误')
#
#         user_dict = user.to_dict()
#         user_login = get_user_login_by_id(user.id)
#         user_dict.update({
#             'username': user_login.username
#         })
#         token_dict = Token.generate_token(user.id)
#
#         data = {
#             'user': user_dict,
#             'token': token_dict,
#         }
#         g.user = user
#         return data


class InvestorMobileLoginAPI(ApiViewHandler):
    @params_required(*['mobile', 'code', 'manager_id'])
    def post(self):
        g.user_operation = '登录-手机号'
        check_sms_captcha(
            verification_code=self.input.code,
            verification_key=self.input.mobile,
        )

        manager = ManagerInfo.get_by_query(manager_id=self.input.manager_id)
        user = get_user_by_mobile(mobile=self.input.mobile)
        if not user:
            user = User.create(
                mobile=self.input.mobile,
                password='',
            )
            user = User.get_by_id(user.id)
        user_dict = user.to_dict()

        if user.last_login_investor:
            chose_investor(user, user.last_login_investor)

        token = Token.generate_token(user.id)
        token.manager_id = self.input.manager_id
        token_dict = token.to_dict()
        token.save()

        data = {
            'user': user_dict,
            'token': token_dict,
        }
        g.user = user
        return data


class Logout(ApiViewHandler):

    @login_required
    def get(self):
        g.token.delete()

    def post(self):
        return self.get()


class RegisterAPI(ApiViewHandler):
    @params_required(*['username', 'password'])
    def post(self):
        if not self.is_valid_password(self.input.password):
            raise VerifyError('Password should contain both numbers and letters,'
                              ' and the length should be between 8-16 bits !')
        register_user(self.input.username, self.input.password)


class Logic(ApiViewHandler):

    def get(self):
        return

