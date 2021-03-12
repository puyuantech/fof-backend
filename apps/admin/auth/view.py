from flask import g, request, current_app
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from bases.constants import StuffEnum
from models import Token, User, ManagerUserMap
from utils.decorators import params_required, login_required
from apps.captchas.libs import check_img_captcha, check_sms_captcha
from .libs import check_username_login


class AdminLoginAPI(ApiViewHandler):
    @params_required(*['username', 'password', 'verification_code', 'verification_key'])
    def post(self):
        g.user_operation = '登录-密码'
        check_img_captcha(
            verification_code=self.input.verification_code,
            verification_key=self.input.verification_key,
        )
        user = check_username_login(
            username=self.input.username,
            password=self.input.password,
        )
        if not user.is_staff:
            raise VerifyError('非管理员')

        m = ManagerUserMap.filter_by_query(
            user_id=user.id,
        ).first()
        if not m:
            raise VerifyError('未找到管理信息')
        user_dict = user.to_dict()

        token = Token.generate_token(user.id)
        token.manager_id = m.manager_id
        token_dict = token.to_dict()
        token.save()

        g.user = user
        g.token = token

        data = {
            'user': user_dict,
            'token': token_dict,
        }
        return data