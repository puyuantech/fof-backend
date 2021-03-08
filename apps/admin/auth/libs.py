from models import User
from bases.exceptions import LogicError


def get_user_by_username(username):
    return User.filter_by_query(username=username).first()


def check_username_login(username, password):
    user = get_user_by_username(username)
    if not user:
        raise LogicError("用户名不存在")
    if not user.check_password(password):
        raise LogicError("密码错误")
    if user.is_deleted:
        raise LogicError("账户已经停用")
    return user
