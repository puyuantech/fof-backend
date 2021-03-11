from flask import g, request

from bases.globals import db
from bases.exceptions import VerifyError
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required, params_required
from utils.helper import replace_nan


class PositionAnalysis(ApiViewHandler):

    @login_required
    def get(self):
        results = db.session.query(

        ).filter(

        ).order_by(

        ).all()
        data = {
            'mv': [],
            'total_ret': [],
            'total_rr': [],
        }
        for i in results:
            data['mv'].append(i.mv)
            data['total_ret'].append(i.total_ret)
            data['total_rr'].append(i.total_rr)

        return replace_nan(data)

