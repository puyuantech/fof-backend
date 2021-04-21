
from pandas import DataFrame

from models import PortfolioTrade
from utils.helper import replace_nan

from .validators.trade import TradeHistoryValidation


def get_title_and_items(df: DataFrame):
    df = df.reset_index().to_dict('list')
    return {
        'title': df.pop('index_id'),
        'items': [{'key': k, 'value': replace_nan(v)} for k, v in df.items()],
    }


def get_trade_history(portfolio_id):
    trade_history = PortfolioTrade.get_by_id(portfolio_id).trade_history
    return TradeHistoryValidation(trade_history=trade_history).dict()['trade_history']


def get_trade_and_benchmark(portfolio_id):
    portfolio_trade = PortfolioTrade.get_by_id(portfolio_id)
    return {
        'trade_history': TradeHistoryValidation(trade_history=portfolio_trade.trade_history).dict()['trade_history'],
        'benchmark_id_info': portfolio_trade.benchmark_id_info,
    }

