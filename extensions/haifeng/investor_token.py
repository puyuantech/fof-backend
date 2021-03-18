
import datetime
import requests

from collections import namedtuple
from flask import current_app

from bases.globals import settings
from models import InvestorInformation
from utils.helper import Singleton


Token = namedtuple('Token', ['token', 'expires_at'])


class InvestorToken(metaclass=Singleton):

    def __init__(self):
        self.host = settings['HAI_FENG_HOST']
        self.tokens = {}

    def generate_new_token(self, user_id, secret):
        endpoint = '/v2/auth/getInvestorToken'
        now = datetime.datetime.now()
        response = requests.post(self.host + endpoint, json={'individualId': user_id, 'secret': secret}, timeout=5)
        data = response.json()
        if data['success'] != 1:
            current_app.logger.error(f'[InvestorToken] Failed to get token! (data){data}')
            return

        token = data['data']['token']
        expires_at = now + datetime.timedelta(hours=12)
        return Token(token, expires_at)

    def get_token(self, investor_id, secret=None):
        if investor_id not in self.tokens or datetime.datetime.now() > self.tokens[investor_id].expires_at:
            if not secret:
                secret = InvestorInformation.get_by_query(investor_id=investor_id).secret
            if not secret:
                return

            new_token = self.generate_new_token(investor_id, secret)
            if not new_token:
                return

            self.tokens[investor_id] = new_token
        return self.tokens[investor_id].token

