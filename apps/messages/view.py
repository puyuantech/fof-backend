import json
from flask import request, g

from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import MessageTask, MessageTaskSub, ManagerWeChatAccount
from utils.decorators import login_required
from utils.celery_tasks import send_nav_msg
from utils.helper import generate_sql_pagination


class ProNavMessageAPI(ApiViewHandler):
    model = MessageTask

    @login_required
    def get(self, fof_id):
        p = generate_sql_pagination()
        query = self.model.filter_by_query(fof_id=fof_id)
        data = p.paginate(query)
        return data

    @login_required
    def post(self, fof_id):
        nav_data = request.json.get('nav_data')
        if nav_data.get('date') is None or nav_data.get('nav') is None or nav_data.get('acc_nav') is None or \
                nav_data.get('pro_name') is None:
            raise VerifyError('净值格式不正确')

        investors = request.json.get('investors', [])
        if not investors:
            raise VerifyError('缺少投资者参数！')

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
            }
        else:
            raise VerifyError('信息类型错误')

        mt_id = MessageTask.create(
            manager_id=g.token.manager_id,
            fof_id=fof_id,
            name=request.json.get('name'),
        ).id

        for i in investors:
            mts = MessageTaskSub.create(
                task_id=mt_id,
                manager_id=g.token.manager_id,
                name=request.json.get('name'),
                task_type=request.json.get('task_type'),
                task_content=json.dumps(nav_data),
                task_to=json.dumps(i),
                task_from=json.dumps(task_from),
                task_status=MessageTaskSub.TaskStatus.PENDING,
            )
            send_nav_msg.delay(mts.id)

        return {
            'task_id': mt_id,
        }


class ProNavSubMessageAPI(ApiViewHandler):
    model = MessageTaskSub

    @login_required
    def get(self, task_id):
        p = generate_sql_pagination()
        query = self.model.filter_by_query(task_id=task_id)
        data = p.paginate(query)
        return data

