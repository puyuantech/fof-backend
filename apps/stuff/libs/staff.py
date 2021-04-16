import datetime
from flask import request, g
from models import User, ManagerUserMap
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


def register_staff_user(username, password):
    if get_user_by_username(username):
        raise VerifyError('用户名已存在！')
    user = User.create(
        staff_name=username,
        username=username,
        password=password,
        is_staff=True,
    )
    ManagerUserMap.create(
        user_id=user.id,
        manager_id=g.token.manager_id,
    )
    return user


def update_user_info(user):
    columns = [
        'staff_name',
        'role_id',
    ]
    # if request.json.get('role_id') and request.json.get('role_id') == 1:
    #     raise VerifyError('不能添加管理员权限!')
    for i in columns:
        if request.json.get(i) is not None:
            user.update(commit=False, **{i: request.json.get(i)})
    user.save()
    return user
