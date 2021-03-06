import json
import datetime
import requests
from bases.globals import settings, db
from models import WeChatToken


class TokenManager:

    def __init__(self, app_id, app_sec, manager_id):
        self.manager_id = manager_id
        self._access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?' \
            'grant_type=client_credential&appid={}&secret={}'.format(app_id, app_sec)

    def generate_new_access_token(self):
        now = datetime.datetime.now()
        res = requests.get(self._access_token_url, timeout=5)
        data = json.loads(res.text)
        if 'errcode' in data:
            print(f'Failed to get access token, errmsg: {data["errmsg"]}')
            return None
        token = data['access_token']
        expires_at = now + datetime.timedelta(seconds=data['expires_in'] - 300)
        return [token, expires_at]

    def generate_new_jsapi_ticket(self):
        jsapi_ticket_url = ("https://api.weixin.qq.com/cgi-bin/ticket/getticket"
            f"?access_token={self.get_wechat_token_from_db('access_token')}&type=jsapi")
        now = datetime.datetime.now()
        res = requests.get(jsapi_ticket_url, timeout=5)
        data = json.loads(res.text)
        if data['errcode'] != 0:
            print(f'Failed to get jsapi ticket, errmsg: {data["errmsg"]}')
            return None
        token = data['ticket']
        expires_at = now + datetime.timedelta(seconds=data['expires_in'] - 300)
        return [token, expires_at]

    def get_wechat_token_from_db(self, token_type='access_token'):
        wechat_token = db.session.query(WeChatToken).with_for_update().filter(
            WeChatToken.token_type == token_type,
            WeChatToken.manager_id == self.manager_id,
        ).one_or_none()

        if wechat_token and datetime.datetime.now() < wechat_token.expires_at:
            return [wechat_token.key, wechat_token.expires_at]

        if token_type == 'access_token':
            res = self.generate_new_access_token()
        elif token_type == 'jsapi_ticket':
            res = self.generate_new_jsapi_ticket()
        else:
            res = None

        if not res:
            return None

        token = res[0]
        expires_at = res[1]
        if not wechat_token:
            wechat_token = WeChatToken(
                key=token,
                expires_at=expires_at,
                token_type=token_type,
                manager_id=self.manager_id,
            )
            db.session.add(wechat_token)
        else:
            wechat_token.key = token
            wechat_token.expires_at = expires_at

        db.session.commit()
        return res


if __name__ == "__main__":
    from apps import create_app
    create_app().app_context().push()
    app_id = settings['WX']['apps']['fof']['app_id']
    app_sec = settings['WX']['apps']['fof']['app_secret']
    manager_id = 'py1'
    print(f'AccessToken: {TokenManager(app_id=app_id, app_sec=app_sec, manager_id=manager_id).get_wechat_token_from_db()}')
    # print(f'JsApiTicket: {TokenManager().get_wechat_token_from_db("jsapi_ticket")}')
