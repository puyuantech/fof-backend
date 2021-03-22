import pandas as pd
import traceback
import datetime
import io
from flask import request, current_app

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import CustomIndex, CustomIndexNav
from utils.decorators import params_required, login_required
from utils.helper import generate_sql_pagination, replace_nan

from surfing.util.calculator import Calculator as SurfingCalculator


class MessageAPI(ApiViewHandler):

    def get(self):
        return


