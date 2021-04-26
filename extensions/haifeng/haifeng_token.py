
import datetime
import requests

from flask import current_app

from bases.globals import settings
from utils.helper import Singleton


class HaiFengToken(metaclass=Singleton):

    def __init__(self):
        self.url = settings['HAI_FENG']['host'] + '/v2/auth/getToken'
        self._user_id = settings['HAI_FENG']['user_id']
        self._secret = settings['HAI_FENG']['secret']

        self.token = None
        self.expires_at = None

    def generate_new_token(self):
        response = requests.post(
            url=self.url,
            json={'userId': self._user_id, 'secret': self._secret},
            timeout=5,
            headers={'userId': str(self._user_id)},
        )

        data = response.json()
        if data['success'] != 1:
            current_app.logger.error(f'[HaiFengToken] Failed to get token! (data){data}')
            return

        return data['data']['token']

    def get_token(self):
        if not self.token or datetime.datetime.now() > self.expires_at:
            new_token = self.generate_new_token()
            if not new_token:
                return

            self.token = new_token
            self.expires_at = datetime.datetime.now() + datetime.timedelta(hours=12)
            current_app.logger.info(f'[HaiFengToken] generate_new_token (expires_at){self.expires_at} (token){self.token}')

        return self.token

    def get_headers(self):
        return {
            'userId': str(self._user_id),
            'authorization': self.get_token(),
        }

