from flask import g
from models import WeChatUnionID
from bases.exceptions import VerifyError


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

