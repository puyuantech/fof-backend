import requests
import json
import logging
from bases.globals import settings
from extensions.wx.token_manager import TokenManager


class WXMsgManager:
    logger = logging.getLogger('WxWorkNotification')

    ALL_PRIVATE_TEMPLATE = 'https://api.weixin.qq.com/cgi-bin/template/get_all_private_template?access_token={}'

    def __init__(self):
        pass

    @classmethod
    def send(cls, url, data):

        try:
            rsp = requests.post(url, data, timeout=3)
            data = json.loads(rsp.text)
            print(data)
            if data['errcode'] == 0:
                cls.logger.debug('[Wxwork] sent successfully')
            elif data['errcode'] == 45009:
                cls.logger.warning('[Wxwork] api freq out of limit (err_msg){}'.format(data['errmsg']))
            else:
                cls.logger.error('[Wxwork] unknown rsp (rsp){}'.format(data))
        except Exception as e:
            cls.logger.error('[Wxwork] exception (err_msg){}'.format(e))

    def get_all_private_template(self):
        print(self.get_access_token())
        self.send(
            self.ALL_PRIVATE_TEMPLATE.format(self.get_access_token()),
            data=None,
        )

    def get_access_token(self):
        return TokenManager().get_wechat_token_from_db()


if __name__ == '__main__':
    from apps import create_app
    create_app().app_context().push()
    WXMsgManager().get_all_private_template()


