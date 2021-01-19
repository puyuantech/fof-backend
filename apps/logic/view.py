import pandas as pd
import traceback
import datetime
from flask import request, current_app

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from utils.decorators import params_required, login_required
from models.from_surfing import HedgeFundNAV


class LogicAPI(ApiViewHandler):

    def get(self):
        a = HedgeFundNAV.filter_by_query().all()
        print(a)
        return

