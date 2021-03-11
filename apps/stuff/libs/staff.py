import datetime
from flask import request
from models import User
from bases.exceptions import VerifyError


def get_user_by_username(username):
    return User.filter_by_query(show_deleted=True, username=username).first()


def get_all_user_info(user_login):
    user_dict = user_login.to_dict(remove_fields_list=['password_hash'])
    user_login.last_login = datetime.datetime.now()
    user_login.save()
    user_info = User.get_by_id(user_login.user_id)
    user_dict.update(user_info.to_dict())
    return user_dict


def get_all_user_info_by_user(user):
    user_dict = user.to_normal_dict()
    return user_dict


def register_staff_user(username, password):
    if get_user_by_username(username):
        raise VerifyError('用户名已存在！')
    user = User.create(
        nick_name=username,
        username=username,
        password=password,
        is_staff=True,
    )
    return user


def update_user_info(user):
    columns = [
        'staff_name',
    ]
    if request.json.get('role_id') and request.json.get('role_id') == 1:
        raise VerifyError('不能添加管理员权限!')
    for i in columns:
        if request.json.get(i) is not None:
            user.update(commit=False, **{i: request.json.get(i)})
    user.save()
    return user

