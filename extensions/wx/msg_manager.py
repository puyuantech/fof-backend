import requests
import json
import logging
from extensions.wx.token_manager import TokenManager
from extensions.wx.msg_template import init_template


class WXMsgManager:
    logger = logging.getLogger('wx_msg_manager')

    LIST_TEMPLATE = 'https://api.weixin.qq.com/cgi-bin/template/get_all_private_template?access_token={}'
    SEND_TEMPLATE = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'

    def __init__(self, app_id, app_sec, manager_id):
        self.app_id = app_id
        self.app_sec = app_sec
        self.manager_id = manager_id

    @classmethod
    def send(cls, url, data):

        try:
            rsp = requests.post(url, data, timeout=3)
            data = json.loads(rsp.text)
            print(data)
            if data.get('errcode'):
                cls.logger.error('[Wxwork] unknown rsp (rsp){}'.format(data))
            return True, None
        except Exception as e:
            cls.logger.error('[Wxwork] exception (err_msg){}'.format(e))
            return False, data

    def get_all_private_template(self):
        self.send(
            self.LIST_TEMPLATE.format(self.get_access_token()),
            data=None,
        )

    def send_template_msg(self, data):
        return self.send(
            self.SEND_TEMPLATE.format(self.get_access_token()),
            data=json.dumps(data),
        )

    def get_access_token(self):
        token = TokenManager(
            app_id=self.app_id,
            app_sec=self.app_sec,
            manager_id=self.manager_id
        ).get_wechat_token_from_db()
        if token:
            return token[0]
        raise Exception('Access token wrong!')


def wx_nav_template(app_id, app_sec, manager_id, open_id, pro_name, nav, acc_nav, date):
    m = WXMsgManager(
        app_id=app_id,
        app_sec=app_sec,
        manager_id=manager_id
    )
    msg = init_template(
        open_id,
        'c3ADcbl-eShFi5xQJioDNFUXCcq36A75IZHrZsjFuuo',
        {
            "first": {
                "value": "尊敬的用户您好:",
                "color": "#173177"
            },
            "keyword1": {
                "value": pro_name,
                "color": "#173177"
            },
            "keyword2": {
                "value": nav,
                "color": "#173177"
            },
            "keyword3": {
                "value": acc_nav,
                "color": "#173177"
            },
            "keyword4": {
                "value": date,
                "color": "#173177"
            },
            "remark": {
                "value": "请查收",
                "color": "#173177"
            }
        },
    )
    return m.send_template_msg(msg)


if __name__ == '__main__':
    from apps import create_app
    create_app().app_context().push()
    # WXMsgManager().get_all_private_template()
    media = 'jRQIxy6E9L86qmtq0q4Rins1ZLAnGpVd8LrCnFJESQ5jrRrTMvvsa2oVPBWxXaGm'



