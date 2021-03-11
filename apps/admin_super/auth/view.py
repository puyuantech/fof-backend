from flask import g, request, current_app
from bases.viewhandler import ApiViewHandler
from models.super_admin import SuperToken, SuperAdmin
from apps.admin_super.decorators import admin_super_login_required
from utils.decorators import params_required
from apps.captchas.libs import check_img_captcha
from .libs import check_username_login


class SuperAdminLoginAPI(ApiViewHandler):
    @params_required(*['username', 'password', 'verification_code', 'verification_key'])
    def post(self):
        check_img_captcha(
            verification_code=self.input.verification_code,
            verification_key=self.input.verification_key,
        )
        admin = check_username_login(
            username=self.input.username,
            password=self.input.password,
        )
        admin_dict = admin.to_dict()

        token = SuperToken.generate_token(admin.id)
        data = {
            'admin': admin_dict,
            'token': token.to_dict(),
        }
        g.token = token
        g.user = admin
        return data


class Logout(ApiViewHandler):

    @admin_super_login_required
    def get(self):
        g.token.delete()

    def post(self):
        return self.get()

