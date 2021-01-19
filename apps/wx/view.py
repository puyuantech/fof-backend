from flask import g
from bases.viewhandler import ApiViewHandler
from bases.globals import settings
from bases.exceptions import VerifyError
from utils.decorators import params_required, login_required
from extensions.wx.union_manager import WXUnionManager

from .libs import check_we_chat_user_exist, bind_we_chat_user


class WXBindUser(ApiViewHandler):

    @login_required
    @params_required(*['code'])
    def post(self):
        if g.user.we_chat:
            raise VerifyError('请先解绑！')

        union_info = WXUnionManager.get_union_id('fof', self.input.code)
        union_id, open_id = union_info['unionid'], union_info.get('openid')

        check_we_chat_user_exist(union_id)
        bind_we_chat_user(union_id, open_id)

    @login_required
    def delete(self):
        wx = g.user.we_chat
        for i in wx:
            i.logic_delete()


class OfficeAPPID(ApiViewHandler):

    def get(self):
        return {
            'app_id': settings['WX']['apps']['fof']['app_id'],
        }

