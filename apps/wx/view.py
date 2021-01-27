import hashlib
import traceback
from xml.etree import ElementTree as ET

from flask import g, make_response, request, current_app
from bases.viewhandler import ApiViewHandler
from bases.globals import settings, db
from bases.exceptions import VerifyError
from utils.decorators import params_required, login_required
from extensions.wx.union_manager import WXUnionManager
from extensions.wx.receive import Msg
from models import User, WeChatUnionID, Token

from .libs import check_we_chat_user_exist, bind_we_chat_user, decode_wx_msg, encode_wx_msg, \
    wx_text, wx_event


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

    @params_required(*['signature', 'timestamp', 'nonce'])
    def post(self):
        xml_text = decode_wx_msg(
            self.input.signature,
            self.input.timestamp,
            self.input.nonce,
        )
        xml_data = ET.fromstring(xml_text)
        rec_msg = Msg(xml_data)

        if rec_msg.MsgType == 'text':
            ret = wx_text(rec_msg, self.input.nonce)
        elif rec_msg.MsgType == 'event':
            ret = wx_event(rec_msg)
        elif rec_msg.MsgType == 'image':
            ret = 'success'
        else:
            ret = 'success'

        current_app.logger.info(ret)
        return make_response('success')


class WxLoginAPI(ApiViewHandler):

    @params_required(*['code'])
    def post(self):
        try:
            union_info = WXUnionManager.get_union_id('fof', self.input.code)
        except Exception:
            raise VerifyError(traceback.format_exc())

        union_id, open_id = union_info['unionid'], union_info.get('openid')
        is_exists, wx_user = check_we_chat_user_exist(union_id)

        try:
            if is_exists:
                user = wx_user.user
            else:
                user = User.create(
                    nick_name=union_info.get('nickname', ''),
                    is_staff=False,
                )
                user.avatar_url = union_info.get('headimgurl')
                WeChatUnionID.create(
                    union_id=union_id,
                    user_id=user.id,
                    open_id=open_id,
                )
                db.session.commit()

            user_dict = user.to_dict()
            token_dict = Token.generate_token(user.id)
            return {
                'user': user_dict,
                'token': token_dict,
            }
        except Exception as e:
            current_app.logger.error('[wx_login] 查询用户数据库失败 (err_msg){}'.format(traceback.format_exc()))
            raise VerifyError('查询用户数据库失败，(err_msg){}'.format(traceback.format_exc()))


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


class WXBindMobile(ApiViewHandler):

    @params_required(*['mobile', 'mobile_code'])
    @login_required
    def post(self):
        if g.user.mobile:
            raise VerifyError('您已经绑定过手机号！')

        return


class OfficeAPPID(ApiViewHandler):

    def get(self):
        return {
            'app_id': settings['WX']['apps']['fof']['app_id'],
        }

