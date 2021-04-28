
import pandas as pd

from surfing.data.api.portfolio import PortfolioDataApi

from bases.exceptions import LogicError
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan

from .libs import get_trade_history
from .validators import PortfolioIdValidation
from .validators.basic import PortfolioNavValidation, PortfolioStatsValidation


class BenchmarkInfoAPI(ApiViewHandler):

    @login_required
    def get(self):
        return PortfolioDataApi().get_portfolio_benchmark_info()


class PortfolioNavAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = PortfolioNavValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        trade_history = get_trade_history(data.pop('portfolio_id'))
        fund_nav = PortfolioDataApi().get_portfolio_nav(trade_history)['净值']
        df = PortfolioDataApi().get_portfolio_mv(fund_nav, trade_history=trade_history, **data)

        df['data'] = replace_nan(df['data'].reset_index().to_dict('list'))
        return df


class PortfolioStatsAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = PortfolioStatsValidation.get_valid_data(self.input)
        trade_history = get_trade_history(data['portfolio_id'])

        fund_nav = PortfolioDataApi().get_portfolio_nav(trade_history)['净值']
        df = PortfolioDataApi().get_portfolio_stats(fund_nav, data['index_id'], trade_history)
        if df is None:
            return
        return replace_nan(df.reset_index().to_dict('list'))


class FundWeightAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = PortfolioIdValidation.get_valid_data(self.input)

        trade_history = get_trade_history(**data)
        fund_wgt = PortfolioDataApi().get_portfolio_nav(trade_history)['各基权重']
        df = PortfolioDataApi().get_port_fund_weight(fund_wgt, trade_history)
        df['基金'] = df['基金'].where(pd.notnull(df['基金']), None)
        df['类型'] = df['类型'].where(pd.notnull(df['类型']), None)
        return {
            '权重': {
                'datetime': replace_nan(df['类型'].index.tolist()),
                '类型': df['类型'].to_dict('list'),
                '基金': df['基金'].to_dict('list'),
            },
            '类型': df['类型对照'],
        }

