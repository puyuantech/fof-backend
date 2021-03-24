import pandas as pd
import traceback
import datetime
from flask import request, current_app, make_response

from bases.globals import db, celery
from bases.viewhandler import ApiViewHandler
from utils.decorators import params_required, login_required
from models import MessageTaskSub, MessageTask


class LogicAPI(ApiViewHandler):

    def get(self):

        return make_response('1')

