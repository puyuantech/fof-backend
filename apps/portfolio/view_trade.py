
from flask import g

from surfing.data.api.basic import BasicDataApi

from bases.viewhandler import ApiViewHandler
from models import PortfolioTrade
from utils.decorators import login_required

from .validators import PortfolioIdValidation
from .validators.trade import PortfolioTradeValidation, PortfolioUpdateValidation

from .libs import create_portfolio, update_portfolio, delete_portfolio


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
        create_portfolio(g.token.manager_id, data)
        return 'success'

    @login_required
    def put(self):
        data = PortfolioUpdateValidation.get_valid_data(self.input)
        update_portfolio(g.token.manager_id, data)
        return 'success'

    @login_required
    def delete(self):
        data = PortfolioIdValidation.get_valid_data(self.input)
        delete_portfolio(g.token.manager_id, data)
        return 'success'


class PortfolioTradeListAPI(ApiViewHandler):

    @login_required
    def get(self):
        trades = PortfolioTrade.filter_by_query(manager_id=g.token.manager_id).all()
        return [trade.to_dict() for trade in trades]

