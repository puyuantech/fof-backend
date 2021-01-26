from flask import g, current_app, request
from models import WeChatUnionID
from bases.exceptions import VerifyError
from bases.globals import settings

from extensions.wx.msg_crypt.msg_crypt import WXBizMsgCrypt


def check_we_chat_user_exist(union_id):
    wx = WeChatUnionID.filter_by_query(
        union_id=union_id,
    ).first()
    if wx:
        raise VerifyError('此微信已绑定账号！')


def bind_we_chat_user(union_id, open_id):
    WeChatUnionID.create(
        user_id=g.user.id,
        union_id=union_id,
        open_id=open_id,
    )


def decode_wx_msg(signature, timestamp, nonce):
    # 解密
    wx_msg_crypt = WXBizMsgCrypt(
        settings['WX']['apps']['fof']['token'],
        settings['WX']['apps']['fof']['aes_key'],
        settings['WX']['apps']['fof']['app_id'],
    )

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
    wx_msg_crypt = WXBizMsgCrypt(
        settings['WX']['apps']['fof']['token'],
        settings['WX']['apps']['fof']['aes_key'],
        settings['WX']['apps']['fof']['app_id'],
    )

    status, xml_data = wx_msg_crypt.EncryptMsg(ret_xml, nonce)
    if status != 0:
        raise VerifyError('加密失败！')

    return xml_data
