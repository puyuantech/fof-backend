
from surfing.data.api.portfolio import PortfolioDataApi

from bases.exceptions import LogicError
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan

from .libs import get_trade_history, get_trade_and_benchmark
from .validators import PortfolioIdValidation
from .validators.subfund import FundRetValidation, FundPosValidation, RetResolveValidation


class FundAlphaAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = PortfolioIdValidation.get_valid_data(self.input)
        trade_and_benchmark = get_trade_and_benchmark(**data)

        return PortfolioDataApi().get_port_fund_alpha_detail(**trade_and_benchmark)


class FundRetAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FundRetValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')
        trade_and_benchmark = get_trade_and_benchmark(data.pop('portfolio_id'))

        df = PortfolioDataApi().get_port_recent_ret_details(**trade_and_benchmark, **data)

        df['组合收益'] = replace_nan(df['组合收益'].reset_index().to_dict('list'))
        df['资产价格比收益'] = replace_nan(df['资产价格比收益'].reset_index().to_dict('list'))
        df['个基近期收益'] = replace_nan(df['个基近期收益'].to_dict('list'))
        return df


class FundIndexAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = PortfolioIdValidation.get_valid_data(self.input)
        trade_history = get_trade_history(**data)
        return {
            'fund_list': PortfolioDataApi().get_port_fund_list(trade_history),
            'index_list': PortfolioDataApi().get_portfolio_benchmark_info(),
        }


class FundPosAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FundPosValidation.get_valid_data(self.input)
        trade_history = get_trade_history(data.pop('portfolio_id'))
        df = PortfolioDataApi().get_port_fund_pos_date(**data, trade_history=trade_history)
        df['净值'] = replace_nan(df['净值'].reset_index().to_dict('list'))
        return df


class ResolveDateAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = PortfolioIdValidation.get_valid_data(self.input)
        trade_history = get_trade_history(**data)
        df = PortfolioDataApi().get_port_ret_resolve_date_range(trade_history)
        return replace_nan(df)


class RetResolveAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = RetResolveValidation.get_valid_data(self.input)
        trade_history = get_trade_history(data.pop('portfolio_id'))
        share_list = PortfolioDataApi().get_portfolio_nav(trade_history)['持有信息']
        return PortfolioDataApi().get_port_ret_resolve(share_list, **data)

