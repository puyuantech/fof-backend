from flask import request, g
from models import ManagerWeChatAccount, ManagerEmailAccount, MessageTaskSub, FOFNotification
from bases.exceptions import VerifyError


def select_task_from():
    task_type = request.json.get('task_type')
    if task_type == MessageTaskSub.TaskType.WE_CHAT:
        acc = ManagerWeChatAccount.filter_by_query(
            manager_id=g.token.manager_id,
        ).one_or_none()
        if not acc:
            raise VerifyError('平台不存在')
        task_from = {
            'app_id': acc.app_id,
            'app_sec': acc.app_sec,
            'manager_id': g.token.manager_id,
            'nav_template_id': acc.nav_template_id,
        }
    elif task_type == MessageTaskSub.TaskType.MAIL:
        acc = ManagerEmailAccount.filter_by_query(
            manager_id=g.token.manager_id,
        ).one_or_none()
        if not acc:
            raise VerifyError('平台不存在')

        task_from = {
            'server': acc.server,
            'port': acc.port,
            'username': acc.username,
            'password': acc.secret,
            'sender': acc.sender,
            'use_ssl': acc.is_ssl,
        }
    elif task_type == MessageTaskSub.TaskType.MOBILE:
        task_from = {}
    elif task_type == MessageTaskSub.TaskType.NAV_NOTIFICATION:
        task_from = {
            'manager_id': g.token.manager_id,
        }
    else:
        raise VerifyError('信息类型错误')

    return task_from

