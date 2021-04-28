import json
import requests
from flask import request, current_app, make_response

from bases.globals import db, celery, cas
from extensions.cas.cas_models.example import CasExample
from bases.viewhandler import ApiViewHandler


class LogicAPI(ApiViewHandler):

    def get(self, _file):
        cas.get_conn()
        a = CasExample.get(user_id=1)
        print(a.to_dict())

        return make_response('1')


class Logic1API(ApiViewHandler):

    def post(self):
        wb = 'https://oapi.dingtalk.com/robot/send?access_token=ab796056fcfdb0b6513e11eb0b2d701c180761909f53f89a1d3d1ba8c7e5d410'
        data = request.json
        data['zabbix'] = 'zabbix'
        message = {
            "msgtype": "text",
            "text": {
                'content': data
            }
        }
        message = json.dumps(message)
        res = requests.post(wb, data=message, timeout=3, headers={
            'Content-Type': 'application/json',
        })
        print(res.text)
        return
