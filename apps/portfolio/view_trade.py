
from flask import g

from surfing.data.api.basic import BasicDataApi

from bases.viewhandler import ApiViewHandler
from models import PortfolioTrade
from utils.decorators import login_required
from utils.helper import replace_nan

from .validators import PortfolioIdValidation
from .validators.trade import PortfolioTradeValidation, PortfolioUpdateValidation


class IndexListAPI(ApiViewHandler):

    @login_required
    def get(self):
        return BasicDataApi().get_asset_benchmark_info_list()


class PortfolioTradeAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = PortfolioIdValidation.get_valid_data(self.input)
        return PortfolioTrade.get_by_query(
            manager_id=g.token.manager_id,
            id=data['portfolio_id'],
        ).to_dict()

    @login_required
    def post(self):
        data = PortfolioTradeValidation.get_valid_data(self.input)
        PortfolioTrade.create(manager_id=g.token.manager_id, **replace_nan(data))
        return 'success'

    @login_required
    def put(self):
        data = PortfolioUpdateValidation.get_valid_data(self.input)
        PortfolioTrade.get_by_query(
            manager_id=g.token.manager_id,
            id=data.pop('portfolio_id'),
        ).update(**replace_nan(data))
        return 'success'

    @login_required
    def delete(self):
        data = PortfolioIdValidation.get_valid_data(self.input)
        PortfolioTrade.get_by_query(
            id=data['portfolio_id'],
            manager_id=g.token.manager_id,
        ).logic_delete()
        return 'success'


class PortfolioTradeListAPI(ApiViewHandler):

    @login_required
    def get(self):
        trades = PortfolioTrade.filter_by_query(manager_id=g.token.manager_id).all()
        return [trade.to_dict() for trade in trades]

