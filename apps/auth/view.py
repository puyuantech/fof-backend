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

    def get(self):
        mobile = request.args.get('mobile')
        if not mobile:
            raise VerifyError('参数不正确！')

        results = db.session.query(
            ManagerInfo
        ).filter(
            User.mobile == mobile,
            UserInvestorMap.user_id == User.id,
            UserInvestorMap.investor_id == InvestorInfo.investor_id,
            UnitMap.investor_id == InvestorInfo.investor_id,
            UnitMap.manager_id == ManagerInfo.manager_id,
        ).all()
        return [i.to_dict() for i in results]

    @params_required(*['mobile', 'code', 'manager_id'])
    def post(self):
        g.user_operation = '登录-手机号'
        check_sms_captcha(
            verification_code=self.input.code,
            verification_key=self.input.mobile,
        )
        # 1. user
        manager = ManagerInfo.get_by_query(manager_id=self.input.manager_id)
        user = get_user_by_mobile(mobile=self.input.mobile)

        if not user:
            user, investor = User.create_main_user_investor(mobile=self.input.mobile)
            investor.create_manager_map(manager.manager_id, mobile=self.input.mobile)
            user = User.get_by_id(user.id)
            user_dict = user.to_dict()
            investor_dict = chose_investor(user, manager, investor_id=investor.investor_id)
        else:
            user_dict = user.to_dict()
            investor = user.get_main_investor()
            if not investor.check_manager_map(manager_id=manager.manager_id):
                investor.create_manager_map(manager_id=manager.manager_id, mobile=self.input.mobile)
                user.last_login_investor = None
            investor_dict = chose_investor(user, manager)

        # 2. token
        token = Token.generate_token(user.id)
        token.manager_id = self.input.manager_id
        token.investor_id = investor_dict['investor_id']
        token_dict = token.to_dict()
        token.save()

        user.last_login_investor = investor_dict['investor_id']
        user.last_login = datetime.datetime.now()
        user.save()

        data = {
            'user': user_dict,
            'token': token_dict,
            'investor': investor_dict,
        }
        g.user = user
        return data


class ChoseInvestor(ApiViewHandler):

    @login_required
    def get(self):
        return get_user_investors(g.user, g.token.manager_id)

    @login_required
    @params_required(*['investor_id'])
    def post(self):
        manager = ManagerInfo.get_by_query(manager_id=g.token.manager_id)

        investor_dict = chose_investor(g.user, manager, investor_id=self.input.investor_id)
        token = Token.generate_token(g.user.id)
        token.manager_id = self.input.manager_id
        token.investor_id = investor_dict['investor_id']
        token_dict = token.to_dict()
        token.save()

        g.user.last_login_investor = investor_dict['investor_id']
        g.user.last_login = datetime.datetime.now()
        g.user.save()

        data = {
            'token': token_dict,
            'investor': investor_dict,
        }
        return data


class Logout(ApiViewHandler):

    @login_required
    def get(self):
        g.token.delete()

    def post(self):
        return self.get()


class Logic(ApiViewHandler):

    def get(self):
        return

