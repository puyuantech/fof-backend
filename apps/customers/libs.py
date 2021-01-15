import datetime
from flask import request
from models import User, UserLogin
from bases.exceptions import VerifyError
from bases.constants import StuffEnum


def get_user_by_username(username):
    return UserLogin.filter_by_query(show_deleted=True, username=username).first()


def get_user_by_mobile(mobile):
    return User.filter_by_query(mobile=mobile).first()


def get_all_user_info_by_user(user):
    user_dict = user.to_cus_dict()

    user_login = UserLogin.filter_by_query(
        user_id=user.id,
    ).first()
    if not user_login:
        return user_dict
    user_dict['username'] = user_login.username
    return user_dict


def register_investor_user(mobile):
    if get_user_by_mobile(mobile):
        raise VerifyError('电话号码已存在！')

    if get_user_by_username(mobile):
        raise VerifyError('用户名已存在！')

    user = User.create(
        nick_name=mobile,
        is_staff=False,
        role_id=StuffEnum.INVESTOR,
        mobile=mobile,
    )
    try:
        user_login = UserLogin.create(
            user_id=user.id,
            username=mobile,
            password='',
        )
    except Exception as e:
        user.delete()
        raise e
    return user, user_login


def update_user_info(user):
    columns = [
        'nick_name',
        'sex',
        'email',
        'avatar_url',
        'site',
        'name',
        'amount',
        'sign_date',
        'sponsor',
        'investor_id',
    ]
    if request.json.get('role_id') and request.json.get('role_id') == 1:
        raise VerifyError('不能添加管理员权限!')
    for i in columns:
        if request.json.get(i) is not None:
            user.update(commit=False, **{i: request.json.get(i)})
    user.save()
    return user




