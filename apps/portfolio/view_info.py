
from flask import g

from surfing.data.api.portfolio import PortfolioDataApi

from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan

from .libs import get_trade_history, get_portfolio_infos
from .validators import PortfolioIdValidation


class PortfolioInfoListAPI(ApiViewHandler):

    @login_required
    def get(self):
        return replace_nan(get_portfolio_infos(g.token.manager_id))


class PortfolioStatusAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = PortfolioIdValidation.get_valid_data(self.input)
        trade_history = get_trade_history(**data)
        df = PortfolioDataApi().calc_port_status(trade_history=trade_history)
        return replace_nan(df)

