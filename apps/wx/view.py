import hashlib
import traceback
import datetime
from xml.etree import ElementTree as ET

from flask import g, make_response, request, current_app
from bases.viewhandler import ApiViewHandler
from bases.globals import settings, db
from bases.exceptions import VerifyError
from utils.decorators import params_required, login_required
from extensions.wx.union_manager import WXUnionManager
from extensions.wx.receive import Msg
from models import User, WeChatUnionID, Token, ManagerWeChatAccount, ManagerInfo
from apps.auth.libs import chose_investor
from apps.captchas.libs import check_sms_captcha
from apps.auth.libs import get_user_by_mobile

from .libs import check_we_chat_user_exist, bind_we_chat_user, decode_wx_msg, encode_wx_msg, \
    wx_text, wx_event, refresh_token


class WX(ApiViewHandler):

    @params_required(*['signature', 'timestamp', 'nonce', 'echostr'])
    def get(self):
        """绑定后台验证时使用"""
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
        """处理用户消息"""
        xml_text = decode_wx_msg(
            self.input.signature,
            self.input.timestamp,
            self.input.nonce,
        )
        xml_data = ET.fromstring(xml_text)
        rec_msg = Msg(xml_data)

        if rec_msg.MsgType == 'text':
            ret = wx_text(rec_msg)
        elif rec_msg.MsgType == 'event':
            ret = wx_event(rec_msg)
        elif rec_msg.MsgType == 'image':
            ret = 'success'
        else:
            ret = 'success'

        current_app.logger.info(ret)
        ret = encode_wx_msg(ret, self.input.nonce)
        return make_response(ret)


class WxLoginAPI(ApiViewHandler):

    @params_required(*['code'])
    def post(self, manager_id):
        acc = ManagerWeChatAccount.filter_by_query(
            manager_id=manager_id,
        ).one_or_none()
        if not acc:
            raise VerifyError('平台不存在')

        try:
            info = WXUnionManager.get_open_id_by_token(acc.app_id, acc.app_sec, self.input.code)
        except Exception:
            raise VerifyError(traceback.format_exc())

        open_id = info.get('openid')
        is_exists, wx_user = check_we_chat_user_exist(open_id, manager_id)
        manager = ManagerInfo.get_by_query(manager_id=self.input.manager_id)

        try:
            if is_exists:
                user = wx_user.user
                investor = user.get_main_investor()
                if not investor.check_manager_map(manager_id=manager.manager_id):
                    investor.create_manager_map(manager_id=manager.manager_id, mobile=self.input.mobile)
                    user.last_login_investor = None
                investor_dict = chose_investor(user, manager)
                return refresh_token(user, investor_dict)

            user = User.create(
                is_staff=False,
                is_wx=True,
            )
            user_dict = user.to_dict()

            WeChatUnionID.create(
                user_id=user.id,
                open_id=open_id,
                nick_name=info.get('nickname'),
                avatar_url=info.get('headimgurl'),
                manager_id=manager_id,
            )

            token = Token.generate_token(user.id)
            token.manager_id = self.input.manager_id
            token_dict = token.to_dict()
            token.save()

            user.last_login = datetime.datetime.now()
            user.save()
            return {
                'user': user_dict,
                'token': token_dict,
            }
        except Exception as e:
            current_app.logger.error('[wx_login] 查询用户数据库失败 (err_msg){}'.format(traceback.format_exc()))
            raise VerifyError('查询用户数据库失败，(err_msg){}'.format(traceback.format_exc()))


class WXBindMobile(ApiViewHandler):

    @params_required(*['mobile', 'mobile_code'])
    @login_required
    def post(self):
        if g.user.mobile:
            raise VerifyError('您已经绑定过手机号！')

        check_sms_captcha(
            verification_code=self.input.mobile_code,
            verification_key=self.input.mobile,
        )
        manager = ManagerInfo.filter_by_query(manager_id=g.token.manager_id)
        target_user = get_user_by_mobile(mobile=self.input.mobile)
        if not target_user:
            user, investor = User.create_main_user_investor(mobile=self.input.mobile)
            investor.create_manager_map(manager.manager_id, mobile=self.input.mobile)
            user = User.get_by_id(user.id)
            investor_dict = chose_investor(user, manager, investor_id=investor.investor_id)
            g.user.mobile = self.input.mobile
            db.session.commit()
            return refresh_token(user, investor_dict)

        if target_user.we_chat:
            raise VerifyError('目标账户已绑定别的微信号！')

        # 绑定新的 User 对象，并删除原虚拟对象
        wx_user = g.user.we_chat[0]
        wx_user.user_id = target_user.id
        g.user.is_deleted = True
        db.session.commit()

        investor = target_user.get_main_investor()
        if not investor.check_manager_map(manager_id=manager.manager_id):
            investor.create_manager_map(manager_id=manager.manager_id, mobile=self.input.mobile)
            target_user.last_login_investor = None
        investor_dict = chose_investor(target_user, manager)
        return refresh_token(target_user, investor_dict)


class OfficeAPPID(ApiViewHandler):

    def get(self):
        return {
            'app_id': settings['WX']['apps']['fof']['app_id'],
        }

