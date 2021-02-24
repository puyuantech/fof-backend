from flask import g, request, current_app
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from bases.constants import StuffEnum
from models import Token
from utils.decorators import params_required, login_required
from apps.captchas.libs import check_img_captcha, check_sms_captcha
from .libs import check_login, get_all_user_info, register_user, get_user_by_mobile, get_user_login_by_id


class LoginAPI(ApiViewHandler):
    @params_required(*['username', 'password', 'verification_code', 'verification_key'])
    def post(self):
        check_img_captcha(
            verification_code=self.input.verification_code,
            verification_key=self.input.verification_key,
        )
        user_login = check_login(
            username=self.input.username,
            password=self.input.password,
        )
        user_dict = get_all_user_info(user_login)
        token_dict = Token.generate_token(user_login.user_id)

        data = {
            'user': user_dict,
            'token': token_dict,
        }
        return data


class MobileLoginAPI(ApiViewHandler):
    @params_required(*['mobile', 'code'])
    def post(self):
        check_sms_captcha(
            verification_code=self.input.code,
            verification_key=self.input.mobile,
        )
        user = get_user_by_mobile(mobile=self.input.mobile)
        if not user:
            raise VerifyError('用户不存在')
        if user.role_id not in [StuffEnum.ADMIN, StuffEnum.OPE_MANAGER, StuffEnum.FUND_MANAGER]:
            raise VerifyError('权限错误')

        user_dict = user.to_dict()
        user_login = get_user_login_by_id(user.id)
        user_dict.update({
            'username': user_login.username
        })
        token_dict = Token.generate_token(user.id)

        data = {
            'user': user_dict,
            'token': token_dict,
        }
        return data


class InvestorMobileLoginAPI(ApiViewHandler):
    @params_required(*['mobile', 'code'])
    def post(self):
        check_sms_captcha(
            verification_code=self.input.code,
            verification_key=self.input.mobile,
        )
        user = get_user_by_mobile(mobile=self.input.mobile)
        if not user:
            raise VerifyError('用户不存在')
        if user.role_id not in [StuffEnum.INVESTOR]:
            raise VerifyError('权限错误')

        user_dict = user.to_dict()
        user_login = get_user_login_by_id(user.id)
        user_dict.update({
            'username': user_login.username
        })
        token_dict = Token.generate_token(user.id)

        data = {
            'user': user_dict,
            'token': token_dict,
        }
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
        current_app.logger.info(request.headers)
        print(request.headers)
        print(request.data)
        print(request)

