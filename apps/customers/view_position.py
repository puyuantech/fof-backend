from flask import g, request

from bases.globals import db
from bases.exceptions import VerifyError
from bases.viewhandler import ApiViewHandler
from models import FOFInvestorPositionSummary
from utils.decorators import login_required, params_required
from utils.helper import replace_nan


class PositionAnalysis(ApiViewHandler):

    @login_required
    def get(self, investor_id):
        results = db.session.query(
            FOFInvestorPositionSummary
        ).filter(
            FOFInvestorPositionSummary.investor_id == investor_id,
            FOFInvestorPositionSummary.manager_id == g.token.manager_id,
        ).order_by(
            FOFInvestorPositionSummary.datetime.asc()
        ).all()
        data = {
            'dates': [],
            'mv': [],
            'total_ret': [],
            'total_rr': [],
        }
        for i in results:
            data['mv'].append(i.mv)
            data['total_ret'].append(i.total_ret)
            data['total_rr'].append(i.total_rr)
            data['dates'].append(i.datetime)

        return replace_nan(data)
