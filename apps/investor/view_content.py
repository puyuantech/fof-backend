
from flask import g

from bases.viewhandler import ApiViewHandler
from models import InfoStatistics
from utils.decorators import login_required

from .validators.content import ContentStatisticsValidation


class ContentStatisticsAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ContentStatisticsValidation.get_valid_data(self.input)
        InfoStatistics.create(
            **data,
            manager_id=g.token.manager_id,
            investor_id=g.token.investor_id,
        )
        return 'success'

