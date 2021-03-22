import datetime
from flask import current_app
from models import CeleryTaskLogs, MessageTaskSub
from bases.globals import celery


@celery.task()
def print_1(_id):
    obj = MessageTaskSub.get_by_id(_id)
    obj.task_status = MessageTaskSub.TaskStatus.SUCCESS
    obj.save()


@celery.task()
def clean_celery_log():
    CeleryTaskLogs.query.filter(
        CeleryTaskLogs.done == 1,
        CeleryTaskLogs.task_status == 1,
        CeleryTaskLogs.update_time < datetime.datetime.now() - datetime.timedelta(days=10)
    ).delete()
    return '清理成功'
