
from surfing.data.api.portfolio import PortfolioDataApi

from bases.exceptions import LogicError
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan

from .validators.income import RetDistributionValidation


class RetDistributionAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = RetDistributionValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        fund_nav = PortfolioDataApi().get_portfolio_nav(trade_history=data.pop('trade_history'))['净值']
        df = PortfolioDataApi().get_portfolio_ret_distribution(fund_nav, **data)

        df['收益'] = replace_nan(df['收益'].reset_index().to_dict('list'))
        return df

