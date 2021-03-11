from models.super_admin import SuperAdmin
from bases.exceptions import LogicError


def get_user_by_username(username):
    return SuperAdmin.filter_by_query(username=username).first()


def check_username_login(username, password):
    admin = get_user_by_username(username)
    if not admin:
        raise LogicError("用户名不存在")
    if not admin.check_password(password):
        raise LogicError("密码错误")
    if admin.is_deleted:
        raise LogicError("账户已经停用")
    return admin
