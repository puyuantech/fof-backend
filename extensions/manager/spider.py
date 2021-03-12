
import urllib3
import requests
import time
import traceback

from flask import current_app

from .parser import ManagementParser


urllib3.disable_warnings()


class ManagementSpider:

    host = 'https://gs.amac.org.cn/amac-infodisc'

    @classmethod
    def get_json(cls, endpoint: str) -> dict:
        try:
            response = requests.post(cls.host + endpoint, json={}, timeout=3, verify=False)
            return response.json()
        except Exception:
            current_app.logger.error(f'[get_json] failed! (endpoint){endpoint} (err_msg){traceback.format_exc()}')
            return {'content': [], 'last': True}

    @classmethod
    def get_html(cls, endpoint: str):
        try:
            response = requests.get(cls.host + endpoint, timeout=3, verify=False)
            response.encoding = 'utf-8'
            return response
        except Exception as e:
            current_app.logger.error(f'[get_html] failed! (endpoint){endpoint} (err_msg){traceback.format_exc()}')
            raise e

    @classmethod
    def get_manager_list(cls):
        endpoint = '/api/pof/manager/query?rand=0.5&page={}&size=1000'
        index = 0
        while True:
            data = cls.get_json(endpoint.format(index))
            yield data['content']
            if data['last']:
                break
            index += 1
            time.sleep(0.5)

    @classmethod
    def get_manager_info(cls, manager_id: str):
        endpoint = f'/res/pof/manager/{manager_id}.html'
        return ManagementParser.parse_manager(cls.get_html(endpoint))

    @classmethod
    def get_fund_info(cls, fund_id: str):
        endpoint = f'/res/pof/fund/{fund_id}.html'
        return ManagementParser.parse_fund(cls.get_html(endpoint))

