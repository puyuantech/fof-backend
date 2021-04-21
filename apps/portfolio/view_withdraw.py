
import pandas as pd

from surfing.data.api.portfolio import PortfolioDataApi

from bases.exceptions import LogicError
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan

from .libs import get_trade_history
from .validators import PortfolioIdValidation, PortfolioWithTimeValidation


class FundMddAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = PortfolioIdValidation.get_valid_data(self.input)
        trade_history = get_trade_history(**data)
        df = PortfolioDataApi().get_port_fund_mdd_details(trade_history)
        return {
            'mdd': df['mdd'].to_dict('list'),
            'fund_nav': replace_nan(df['fund_nav'].where(pd.notnull(df['fund_nav']), None).reset_index().to_dict('list')),
        }


class CurMddAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = PortfolioWithTimeValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        trade_history = get_trade_history(data.pop('portfolio_id'))
        fund_nav = PortfolioDataApi().get_portfolio_nav(trade_history)['净值']
        df = PortfolioDataApi().get_portfolio_cur_mdd(fund_nav, **data)

        df['历史回撤'] = replace_nan(df['历史回撤'].reset_index().to_dict('list'))
        return df

