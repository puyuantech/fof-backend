import datetime
import json
from flask import current_app
from models import CeleryTaskLogs, MessageTaskSub
from bases.globals import celery
from extensions.wx.msg_manager import wx_nav_template


@celery.task()
def send_nav_msg(sub_task_id):
    t = MessageTaskSub.get_by_id(sub_task_id)
    if not t:
        raise Exception('No correct sub task')

    nav_data = json.loads(t.task_content)
    investor = json.loads(t.task_to)
    task_from = json.loads(t.task_from)

    try:
        if t.task_type == MessageTaskSub.TaskType.WE_CHAT:
            if not investor.get('wx_open_id'):
                raise Exception('No wechat open id')

            status, msg = wx_nav_template(
                app_id=task_from.get('app_id'),
                app_sec=task_from.get('app_sec'),
                manager_id=task_from.get('manager_id'),
                open_id=investor.get('wx_open_id'),
                pro_name=nav_data.get('pro_name'),
                nav=nav_data.get('nav'),
                acc_nav=nav_data.get('acc_nav'),
                date=nav_data.get('date'),
            )
            if status:
                t.task_status = MessageTaskSub.TaskStatus.SUCCESS
                return
            t.task_status = MessageTaskSub.TaskStatus.FAILED
            t.err_msg = str(msg)
            return
    except Exception as e:
        t.err_msg = str(e)
        t.task_status = MessageTaskSub.TaskStatus.FAILED
        t.save()
        raise e


@celery.task()
def clean_celery_log():
    CeleryTaskLogs.query.filter(
        CeleryTaskLogs.done == 1,
        CeleryTaskLogs.task_status == 1,
        CeleryTaskLogs.update_time < datetime.datetime.now() - datetime.timedelta(days=10)
    ).delete()
    return '清理成功'
