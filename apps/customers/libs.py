import datetime
from flask import request
from models import User, UserLogin
from bases.exceptions import VerifyError


def get_user_by_username(username):
    return UserLogin.filter_by_query(show_deleted=True, username=username).first()


def get_all_user_info(user_login):
    user_dict = user_login.to_dict(remove_fields_list=['password_hash'])
    user_login.last_login = datetime.datetime.now()
    user_login.save()
    user_info = User.get_by_id(user_login.user_id)
    user_dict.update(user_info.to_dict())
    return user_dict


def get_all_user_info_by_user(user):
    user_dict = user.to_normal_dict()

    user_login = UserLogin.filter_by_query(
        user_id=user.id,
    ).first()
    if not user_login:
        return user_dict
    user_dict['username'] = user_login.username
    return user_dict


def register_staff_user(username, password):
    if get_user_by_username(username):
        raise VerifyError('用户名已存在！')
    user = User.create(
        nick_name=username,
        is_staff=True,
    )
    try:
        user_login = UserLogin.create(
            user_id=user.id,
            username=username,
            password=password,
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
        'role_id',
        'mobile'
    ]
    if request.json.get('role_id') and request.json.get('role_id') == 1:
        raise VerifyError('不能添加管理员权限!')
    for i in columns:
        if request.json.get(i) is not None:
            user.update(commit=False, **{i: request.json.get(i)})
    user.save()
    return user




