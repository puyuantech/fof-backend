from flask import Blueprint
from flask_restful import Api

from .view_asset import FundNavAPI, IndexInfoAPI, RollingCorrAPI, RollingBetaAPI
from .view_basic import BenchmarkInfoAPI, PortfolioNavAPI, PortfolioStatsAPI, FundWeightAPI
from .view_income import RetDistributionAPI
from .view_info import PortfolioInfoListAPI, PortfolioStatusAPI
from .view_subfund import FundAlphaAPI, FundRetAPI, FundIndexAPI, FundPosAPI, ResolveDateAPI, RetResolveAPI
from .view_trade import IndexListAPI, PortfolioTradeAPI, PortfolioTradeListAPI
from .view_withdraw import FundMddAPI, CurMddAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/portfolio')
api = Api(blu)

api.add_resource(FundNavAPI, '/asset/fund_nv')
api.add_resource(IndexInfoAPI, '/asset/index_list')
api.add_resource(RollingCorrAPI, '/asset/rolling_corr')
api.add_resource(RollingBetaAPI, '/asset/rolling_beta')

api.add_resource(BenchmarkInfoAPI, '/basic/benchmark_info')
api.add_resource(PortfolioNavAPI, '/basic/portfolio_nav')
api.add_resource(PortfolioStatsAPI, '/basic/portfolio_stats')
api.add_resource(FundWeightAPI, '/basic/fund_weight')

api.add_resource(RetDistributionAPI, '/income/ret_distribution')

api.add_resource(PortfolioInfoListAPI, '/info/list')
api.add_resource(PortfolioStatusAPI, '/info/status')

api.add_resource(FundAlphaAPI, '/subfund/fund_alpha')
api.add_resource(FundRetAPI, '/subfund/fund_ret')
api.add_resource(FundIndexAPI, '/subfund/fund_index')
api.add_resource(FundPosAPI, '/subfund/fund_pos')
api.add_resource(ResolveDateAPI, '/subfund/resolve_date')
api.add_resource(RetResolveAPI, '/subfund/ret_resolve')

api.add_resource(IndexListAPI, '/trade/index_list')
api.add_resource(PortfolioTradeAPI, '/trade')
api.add_resource(PortfolioTradeListAPI, '/trade/list')

api.add_resource(FundMddAPI, '/withdraw/fund_mdd')
api.add_resource(CurMddAPI, '/withdraw/cur_mdd')
