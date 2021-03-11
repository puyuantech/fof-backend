import functools
from flask import request, g
from bases.exceptions import AuthError


def admin_super_login_required(func):
    @functools.wraps(func)
    def _func_wrapper(cls, *args, **kwargs):
        from apps.admin_super.auth.authtoken import TokenAuthentication
        admin, token = TokenAuthentication().authenticate(request)
        if not admin:
            raise AuthError('请先登录')
        g.admin = admin
        g.token = token

        return func(cls, *args, **kwargs)
    return _func_wrapper

