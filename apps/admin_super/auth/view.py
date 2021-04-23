from flask import g, request, current_app
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models.super_admin import SuperToken, SuperAdmin
from apps.admin_super.decorators import admin_super_login_required
from apps.captchas.libs import check_img_captcha
from extensions.s3.pdf_store import PdfStore
from utils.decorators import params_required

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


class FileParseAPI(ApiViewHandler):

    @admin_super_login_required
    def post(self):
        """将私有文件路径转换为临时可访问路径"""

        file_key = request.json.get('file_key')
        if not file_key:
            raise VerifyError('No file_key')

        return PdfStore().create_pre_signed_url(object_name=file_key)


class Logout(ApiViewHandler):

    @admin_super_login_required
    def get(self):
        g.token.delete()

    def post(self):
        return self.get()

