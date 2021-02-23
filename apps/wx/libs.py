from flask import g, current_app, request
from models import WeChatUnionID
from bases.exceptions import VerifyError
from bases.globals import settings
from extensions.wx.reply import TextMsg, News
from extensions.wx.msg_crypt.msg_crypt import WXBizMsgCrypt

from .constants import WX_REDIRECT_URL

wx_msg_crypt = WXBizMsgCrypt(
    settings['WX']['apps']['fof']['token'],
    settings['WX']['apps']['fof']['aes_key'],
    settings['WX']['apps']['fof']['app_id'],
)


def check_we_chat_user_exist(union_id):
    wx = WeChatUnionID.filter_by_query(
        union_id=union_id,
    ).first()
    if wx:
        return True, wx
    return False, None


def bind_we_chat_user(union_id, open_id):
    WeChatUnionID.create(
        user_id=g.user.id,
        union_id=union_id,
        open_id=open_id,
    )


def decode_wx_msg(signature, timestamp, nonce):
    # 解密
    data = request.get_data(as_text=True)
    status, xml_data = wx_msg_crypt.DecryptMsg(
        data,
        signature,
        timestamp,
        nonce,
    )
    if status != 0:
        current_app.logger.error(status)
        raise VerifyError('解密失败！')

    return xml_data


def encode_wx_msg(ret_xml, nonce):
    # 加密
    status, xml_data = wx_msg_crypt.EncryptMsg(ret_xml, nonce)
    if status != 0:
        raise VerifyError('加密失败！')

    return xml_data


def wx_bind_mobile_news(to_user, from_user):
    new = News(
        to_user,
        from_user,
        '欢迎来到FOF管理系统',
        '点击绑定账号，\n获取实时通知👉👉',
        'https://fof.prism-advisor.com/img/logo-small.d3ee3c36.png',
        WX_REDIRECT_URL.format(
            settings['WX']['apps']['fof']['app_id'],
            'https://fof.prism-advisor.com/wx-bind-mobile'
        ),
    )
    return new.results()


def wx_text(rec_msg):
    input_content = rec_msg.find('Content')
    if input_content == '绑定手机号':
        ret_xml = wx_bind_mobile_news(
            rec_msg.FromUserName,
            rec_msg.ToUserName,
        )
    else:
        content = '您好，您有什么问题需要咨询呢，请留言您的问题、微信号、电话，我们将尽快与您联系。'
        ret_xml = TextMsg(rec_msg.FromUserName, rec_msg.ToUserName, content).results()
    return ret_xml


def wx_event(rec_msg):
    msg_event = rec_msg.find('Event')
    if msg_event == 'SCAN':
        return 'success'
    elif msg_event == 'subscribe':
        ret_xml = wx_bind_mobile_news(
            rec_msg.FromUserName,
            rec_msg.ToUserName,
        )
        return ret_xml

    return 'success'

