import pandas as pd
import traceback
import datetime
from flask import request, current_app

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from utils.decorators import params_required, login_required
from models.from_surfing import MngInfo, HedgeFundNAV, HedgeFundInfo


class LogicAPI(ApiViewHandler):

    def get(self):
        # a = db.session.query(MngInfo).first()
        a = db.session.query(HedgeFundNAV).first()
        # a = db.session.query(HedgeFundInfo).first()



        print(a)
        return

