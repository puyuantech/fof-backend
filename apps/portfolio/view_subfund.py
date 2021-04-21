
from surfing.data.api.portfolio import PortfolioDataApi

from bases.exceptions import LogicError
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan

from .validators import TradeHistoryValidation
from .validators.subfund import FundAlphaValidation, FundRetValidation, FundPosValidation, RetResolveValidation


class FundAlphaAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FundAlphaValidation.get_valid_data(self.input)

        return PortfolioDataApi().get_port_fund_alpha_detail(**data)


class FundRetAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FundRetValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = PortfolioDataApi().get_port_recent_ret_details(**data)

        df['组合收益'] = replace_nan(df['组合收益'].reset_index().to_dict('list'))
        df['资产价格比收益'] = replace_nan(df['资产价格比收益'].reset_index().to_dict('list'))
        df['个基近期收益'] = replace_nan(df['个基近期收益'].to_dict('list'))
        return df


class FundIndexAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = TradeHistoryValidation.get_valid_data(self.input)
        return {
            'fund_list': PortfolioDataApi().get_port_fund_list(**data),
            'index_list': PortfolioDataApi().get_portfolio_benchmark_info(),
        }


class FundPosAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FundPosValidation.get_valid_data(self.input)
        df = PortfolioDataApi().get_port_fund_pos_date(**data)
        df['净值'] = replace_nan(df['净值'].reset_index().to_dict('list'))
        return df


class ResolveDateAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = TradeHistoryValidation.get_valid_data(self.input)
        df = PortfolioDataApi().get_port_ret_resolve_date_range(**data)
        return replace_nan(df)


class RetResolveAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = RetResolveValidation.get_valid_data(self.input)
        share_list = PortfolioDataApi().get_portfolio_nav(trade_history=data.pop('trade_history'))['持有信息']
        return PortfolioDataApi().get_port_ret_resolve(share_list, **data)

