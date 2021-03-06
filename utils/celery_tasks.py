import datetime
import json
from models import CeleryTaskLogs, MessageTaskSub, FOFNotification, ApplyFile, ApplyStatus
from bases.globals import celery
from bases.globals import settings
from extensions.wx.msg_manager import wx_nav_template
from extensions.mail.template import mail_nav_template, mail_admin_failed_sign_template, \
    mail_admin_success_sign_template, mail_captcha_code
from extensions.mengwang.sms import sms_nav_template


@celery.task()
def send_captcha_code_msg(send_to, code):
    mail_captcha_code(
        settings['MAIL_SERVER'],
        settings['MAIL_EMAIL'],
        settings['MAIL_PASSWORD'],
        settings['MAIL_PORT'],
        settings['MAIL_SSL'],
        settings['MAIL_SENDER'],
        '邮箱验证',
        send_to,
        code,
    )


@celery.task()
def send_sign_failed_msg(apply_id, status_id):
    t = ApplyFile.get_by_id(apply_id)
    if not t:
        raise Exception('No correct apply file')
    s = ApplyStatus.get_by_id(status_id)
    if not s:
        raise Exception('No correct apply status')

    mail_admin_failed_sign_template(
        settings['MAIL_SERVER'],
        settings['MAIL_EMAIL'],
        settings['MAIL_PASSWORD'],
        settings['MAIL_PORT'],
        settings['MAIL_SSL'],
        settings['MAIL_SENDER'],
        '审核通知',
        t.email,
        t.manager_name,
        s.failed_reason,
    )


@celery.task()
def send_sign_success_msg(apply_id, admin_name, admin_password):
    t = ApplyFile.get_by_id(apply_id)
    if not t:
        raise Exception('No correct apply file')

    mail_admin_success_sign_template(
        settings['MAIL_SERVER'],
        settings['MAIL_EMAIL'],
        settings['MAIL_PASSWORD'],
        settings['MAIL_PORT'],
        settings['MAIL_SSL'],
        settings['MAIL_SENDER'],
        '审核通知',
        t.email,
        t.manager_name,
        admin_name,
        admin_password,
    )


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
                pro_name=nav_data.get('desc_name'),
                nav=nav_data.get('nav'),
                acc_nav=nav_data.get('acc_nav'),
                date=nav_data.get('date'),
                nav_template_id=task_from.get('nav_template_id'),
            )
            if status:
                t.task_status = MessageTaskSub.TaskStatus.SUCCESS
                return
            t.task_status = MessageTaskSub.TaskStatus.FAILED
            t.err_msg = str(msg)
            return

        if t.task_type == MessageTaskSub.TaskType.MAIL:
            if not investor.get('email'):
                raise Exception('No email')

            mail_nav_template(
                server=task_from.get('server'),
                username=task_from.get('username'),
                password=task_from.get('password'),
                port=task_from.get('port'),
                sender=task_from.get('sender'),
                use_ssl=task_from.get('use_ssl'),
                title='净值提醒',
                send_to=investor.get('email'),
                pro_name=nav_data.get('desc_name'),
                nav=nav_data.get('nav'),
                acc_nav=nav_data.get('acc_nav'),
                date=nav_data.get('date'),
            )
            t.task_status = MessageTaskSub.TaskStatus.SUCCESS
            return

        if t.task_type == MessageTaskSub.TaskType.MOBILE:
            if not investor.get('mobile'):
                raise Exception('No mobile')

            sms_nav_template(
                send_to=investor.get('mobile'),
                pro_name=nav_data.get('desc_name'),
                nav=nav_data.get('nav'),
                acc_nav=nav_data.get('acc_nav'),
                date=nav_data.get('date'),
            )
            t.task_status = MessageTaskSub.TaskStatus.SUCCESS
            return

        if t.task_type == MessageTaskSub.TaskType.NAV_NOTIFICATION:
            FOFNotification.send_nav_update(
                manager_id=task_from.get('manager_id'),
                investor_id=investor.get('investor_id'),
                content={
                    'fof_name': nav_data.get('desc_name'),
                    'fof_id': nav_data.get('fof_id'),
                    'nav': nav_data.get('nav'),
                    'acc_nav': nav_data.get('acc_nav'),
                    'date': nav_data.get('date'),
                }
            )
            t.task_status = MessageTaskSub.TaskStatus.SUCCESS
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
