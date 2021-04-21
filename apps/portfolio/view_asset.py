
from surfing.data.api.portfolio import PortfolioDataApi
from surfing.util.calculator import Calculator

from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan

from .libs import get_title_and_items
from .validators import TradeHistoryValidation
from .validators.asset import RollingValidation


class FundNavAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = TradeHistoryValidation.get_valid_data(self.input)

        df = PortfolioDataApi().get_portfolio_nav(**data)['大类净值']
        return replace_nan(df.reset_index().to_dict('list'))


class IndexInfoAPI(ApiViewHandler):

    @login_required
    def get(self):
        return PortfolioDataApi().get_port_rolling_beta_index_info()


class RollingCorrAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = RollingValidation.get_valid_data(self.input)

        fund_navs = PortfolioDataApi().get_portfolio_nav(trade_history=data.pop('trade_history'))['大类净值']
        df = Calculator.get_product_rolling_corr(fund_navs, **data)

        return {
            'data': replace_nan(df['data'].reset_index().to_dict('list')),
            'details': {key: get_title_and_items(value) for key, value in df['details'].items()},
        }


class RollingBetaAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = RollingValidation.get_valid_data(self.input)

        fund_navs = PortfolioDataApi().get_portfolio_nav(trade_history=data.pop('trade_history'))['大类净值']
        df = Calculator.get_product_rolling_beta(fund_navs, **data)

        return replace_nan(df.reset_index().to_dict('list'))

