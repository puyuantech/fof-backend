import hashlib
import re
from flask import g, request, current_app, make_response
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import ManagerWeChatAccount
from utils.decorators import params_required, login_required
from extensions.wx.token_manager import TokenManager


class ManagerWxAPI(ApiViewHandler):
    @params_required(*['signature', 'timestamp', 'nonce', 'echostr'])
    def get(self, manager_id):
        """绑定后台验证时使用"""
        acc = ManagerWeChatAccount.filter_by_query(
            manager_id=manager_id,
        ).one_or_none()
        if not acc:
            raise VerifyError('验证错误')

        token = acc.token
        access_list = [token, self.input.timestamp, self.input.nonce]
        access_list.sort()
        sha1 = hashlib.sha1()
        sha1.update(access_list[0].encode("utf-8"))
        sha1.update(access_list[1].encode("utf-8"))
        sha1.update(access_list[2].encode("utf-8"))
        hashcode = sha1.hexdigest()

        if hashcode == self.input.signature:
            ret = str(self.input.echostr)
        else:
            ret = ""

        return make_response(ret)


class MWeChatSettingFileAPI(ApiViewHandler):

    def get(self, file_name):
        value = re.findall('^MP_verify_(.*).txt$', file_name)[0]
        response = make_response(value)
        response.headers["Content-Disposition"] = "attachment; filename=%s" % file_name
        response.headers["Content-type"] = "text/plain"
        return response


class WeChatVerifyAPI(ApiViewHandler):

    @params_required(*['app_id', 'app_sec'])
    @login_required
    def post(self):
        t = TokenManager(
            app_id=self.input.app_id,
            app_sec=self.input.app_sec,
            manager_id=g.token.manager_id,
        )
        status = t.generate_new_access_token()
        if not status:
            raise VerifyError('验证失败，请检查配置！')
        return 'success'


class WeChatSettingAPI(ApiViewHandler):
    update_columns = [
        'app_id',
        'app_sec',
        'token',
        'encoding_aes_key',
        'nav_template_id',
    ]

    @login_required
    def get(self):
        obj = ManagerWeChatAccount.filter_by_query(
            manager_id=g.token.manager_id,
        ).first()
        if not obj:
            return {}
        return obj.to_dict()

    @login_required
    def post(self):
        obj = ManagerWeChatAccount.filter_by_query(
            manager_id=g.token.manager_id,
        ).first()
        if not obj:
            ManagerWeChatAccount.create(
                manager_id=g.token.manager_id,
                app_id=request.json.get('app_id'),
                app_sec=request.json.get('app_sec'),
                token=request.json.get('token'),
                encoding_aes_key=request.json.get('encoding_aes_key'),
                nav_template_id=request.json.get('nav_template_id'),
            )
            return 'success'
        for i in self.update_columns:
            if request.json.get(i) is not None:
                obj.update(commit=False, **{i: request.json.get(i)})
        obj.save()
        g.user_operation = '修改微信设置'

    @login_required
    def delete(self):
        obj = ManagerWeChatAccount.filter_by_query(
            manager_id=g.token.manager_id,
        ).first()
        if not obj:
            return {}
        obj.delete()
