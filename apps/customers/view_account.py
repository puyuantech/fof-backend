from flask import g, request

from bases.globals import db
from bases.exceptions import VerifyError
from bases.viewhandler import ApiViewHandler
from models import FOFInvestorPositionSummary
from utils.decorators import login_required, params_required
from utils.helper import replace_nan


class AddSubAccount(ApiViewHandler):

    @login_required
    def get(self, investor_id):
        pass
