import requests
import json
import logging
from extensions.wx.token_manager import TokenManager


class WXMsgManager:
    logger = logging.getLogger('wx_msg_manager')

    LIST_TEMPLATE = 'https://api.weixin.qq.com/cgi-bin/template/get_all_private_template?access_token={}'
    SEND_TEMPLATE = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'

    def __init__(self):
        pass

    @classmethod
    def send(cls, url, data):

        try:
            rsp = requests.post(url, data, timeout=3)
            data = json.loads(rsp.text)
            print(data)
            if data.get('errcode'):
                cls.logger.error('[Wxwork] unknown rsp (rsp){}'.format(data))
        except Exception as e:
            cls.logger.error('[Wxwork] exception (err_msg){}'.format(e))

    def get_all_private_template(self):
        self.send(
            self.LIST_TEMPLATE.format(self.get_access_token()),
            data=None,
        )

    def send_template_msg(self, data):
        self.send(
            self.SEND_TEMPLATE.format(self.get_access_token()),
            data=data,
        )

    def get_access_token(self):
        token = TokenManager().get_wechat_token_from_db()
        if token:
            return token[0]
        raise Exception('Access token wrong!')


if __name__ == '__main__':
    from apps import create_app
    create_app().app_context().push()
    WXMsgManager().get_all_private_template()


