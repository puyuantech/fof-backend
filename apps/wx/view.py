import hashlib
from xml.etree import ElementTree

from flask import g, make_response, request
from bases.viewhandler import ApiViewHandler
from bases.globals import settings
from bases.exceptions import VerifyError
from utils.decorators import params_required, login_required
from extensions.wx.union_manager import WXUnionManager
from extensions.wx.receive import Msg
from extensions.wx.reply import TextMsg, ImageMsg

from .libs import check_we_chat_user_exist, bind_we_chat_user


class WX(ApiViewHandler):

    @params_required(*['signature', 'timestamp', 'nonce', 'echostr'])
    def get(self):
        token = settings['WX']['apps']['fof']['token']

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

    def post(self):
        data = request.get_data(as_text=True)
        xml_data = ElementTree.fromstring(data)
        print(xml_data)

        rec_msg = Msg(xml_data)

        if rec_msg.MsgType == 'text':
            input_content = rec_msg.find('Content').decode('utf-8')
            ret = TextMsg(rec_msg.FromUserName, rec_msg.ToUserName, input_content)
        elif rec_msg.MsgType == 'event':
            pass
        elif rec_msg.MsgType == 'image':
            pass
        else:
            ret = '您好'

        return make_response(ret)


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

