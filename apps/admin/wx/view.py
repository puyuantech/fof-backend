import hashlib
from flask import g, request, current_app, make_response
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import ManagerWeChatAccount
from utils.decorators import params_required, login_required


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


class WeChatSettingAPI(ApiViewHandler):
    update_columns = [
        'app_id',
        'app_sec',
        'token',
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
            )
            return 'success'
        for i in self.update_columns:
            if request.json.get(i) is not None:
                obj.update(commit=False, **{i: request.json.get(i)})
        obj.save()

    @login_required
    def delete(self):
        obj = ManagerWeChatAccount.filter_by_query(
            manager_id=g.token.manager_id,
        ).first()
        if not obj:
            return {}
        obj.delete()
