
import datetime
import requests

from collections import namedtuple
from flask import current_app

from bases.globals import settings
from models import ManagerSecret
from utils.helper import Singleton


Token = namedtuple('Token', ['token', 'expires_at'])


class ManagerToken(metaclass=Singleton):

    def __init__(self):
        self.host = settings['HAI_FENG_HOST']
        self.tokens = {}

    def generate_new_token(self, user_id, secret):
        endpoint = '/v2/auth/getToken'
        now = datetime.datetime.now()
        response = requests.post(self.host + endpoint, json={'userId': user_id, 'secret': secret}, timeout=5)
        data = response.json()
        if data['success'] != 1:
            current_app.logger.error(f'[ManagerToken] Failed to get token! (data){data}')
            return

        token = data['data']['token']
        expires_at = now + datetime.timedelta(hours=12)
        return Token(token, expires_at)

    def get_token(self, manager_id, manager_secret=None):
        if manager_id not in self.tokens or datetime.datetime.now() > self.tokens[manager_id].expires_at:
            if not manager_secret:
                manager_secret = ManagerSecret.get_by_query(manager_id=manager_id)
            new_token = self.generate_new_token(manager_secret.user_id, manager_secret.secret)
            if not new_token:
                return

            self.tokens[manager_id] = new_token
        return self.tokens[manager_id].token

    def get_headers(self, manager_id):
        manager_secret = ManagerSecret.get_by_query(manager_id=manager_id)
        return {
            'userId': str(manager_secret.user_id),
            'authorization': str(self.get_token(manager_id, manager_secret)),
        }

