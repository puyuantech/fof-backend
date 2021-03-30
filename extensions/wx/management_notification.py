
import datetime
import json
import requests

from flask import current_app

from bases.globals import settings


class ManagementNotification:

    webhook_url = settings['MANAGEMENT_WEBHOOK']

    @classmethod
    def send(cls, content):
        message = {
            'msgtype': 'markdown',
            'markdown': {
                'content': content
            }
        }

        try:
            rsp = requests.post(cls.webhook_url, json=message, timeout=3)

            data = json.loads(rsp.text)
            if data['errcode'] == 0:
                current_app.logger.debug('[Wxwork] sent successfully')
            elif data['errcode'] == 45009:
                current_app.logger.warning('[Wxwork] api freq out of limit (err_msg){}'.format(data['errmsg']))
            else:
                current_app.logger.error('[Wxwork] unknown rsp (rsp){}'.format(data))
        except Exception as e:
            current_app.logger.error('[Wxwork] exception (err_msg){}'.format(e))

    @staticmethod
    def parse_failed_count(failed_count):
        color = 'red' if failed_count > 0 else 'info'
        return f'**<font color="{color}">{failed_count}</font>**'

    @classmethod
    def send_update(cls, title, failed_count, managements, exceptions):
        if not cls.webhook_url:
            return

        content = f'**{title}**\n' +\
                  f'>更新时间: <font color="blue">{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</font>\n' +\
                  f'>失败数量: {cls.parse_failed_count(failed_count)}\n'
        if failed_count > 0:
            content += f'>ID列表: [managements]({managements})\n' +\
                       f'>异常日志: [exceptions]({exceptions})\n'

        cls.send(content)

    @classmethod
    def send_manager_update(cls, failed_count=0, managements=None, exceptions=None):
        return cls.send_update('私募管理人更新通知', failed_count, managements, exceptions)

    @classmethod
    def send_fund_update(cls, failed_count=0, managements=None, exceptions=None):
        return cls.send_update('私募管理人产品更新通知', failed_count, managements, exceptions)

