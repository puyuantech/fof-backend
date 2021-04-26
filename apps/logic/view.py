import pandas as pd
import traceback
import datetime
from flask import request, current_app, make_response

from bases.globals import db, celery, cas
from extensions.cas.cas_models.example import CasExample
from bases.viewhandler import ApiViewHandler
from utils.decorators import params_required, login_required
from models import MessageTaskSub, MessageTask


class LogicAPI(ApiViewHandler):

    def get(self, _file):
        cas.get_conn()
        a = CasExample.get(user_id=1)
        print(a.to_dict())

        return make_response('1')

