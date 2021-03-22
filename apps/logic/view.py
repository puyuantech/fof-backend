import pandas as pd
import traceback
import datetime
from flask import request, current_app

from bases.globals import db, celery
from utils.celery_tasks import print_1
from bases.viewhandler import ApiViewHandler
from utils.decorators import params_required, login_required
from models import MessageTaskSub, MessageTask


class LogicAPI(ApiViewHandler):

    def get(self):
        obj = MessageTaskSub.create(
            task_id=1,
            task_type=1,
        )
        print_1.delay(obj.id)
        return

