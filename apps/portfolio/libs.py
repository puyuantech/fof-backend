
import datetime
import traceback

from flask import current_app
from pandas import DataFrame

from surfing.data.api.portfolio import PortfolioDataApi

from bases.exceptions import LogicError
from bases.globals import cas, db
from extensions.cas.cas_models.production import ProductionInfoCas
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


def calc_portfolio_info(trade_history, benchmark_id_info):
    return PortfolioDataApi().get_port_info(trade_history, benchmark_id_info)


def create_portfolio(manager_id, data):
    cas.init_conn()
    portfolio_trade = PortfolioTrade.create(manager_id=manager_id, **replace_nan(data))
    try:
        portfolio_info = calc_portfolio_info(data['trade_history'], portfolio_trade.benchmark_id_info)
        ProductionInfoCas.create_info(portfolio_trade, portfolio_info)
    except Exception:
        portfolio_trade.delete()
        current_app.logger.error(f'[create portfolio] failed! (err){traceback.format_exc()}')
        raise LogicError('创建组合失败！')


def update_portfolio(manager_id, data):
    cas.init_conn()
    portfolio_trade = PortfolioTrade.get_by_query(manager_id=manager_id, id=data.pop('portfolio_id'))
    try:
        portfolio_trade.update(**replace_nan(data))
        portfolio_info = calc_portfolio_info(data['trade_history'], portfolio_trade.benchmark_id_info)
        ProductionInfoCas.update_info(portfolio_trade, portfolio_info, portfolio_trade.update_time)
    except Exception:
        db.session.rollback()
        current_app.logger.error(f'[update portfolio] failed! (err){traceback.format_exc()}')
        raise LogicError('更新组合失败！')


def delete_portfolio(manager_id, data):
    cas.init_conn()
    portfolio_trade = PortfolioTrade.get_by_query(manager_id=manager_id, id=data['portfolio_id'])
    try:
        portfolio_trade.logic_delete()
        ProductionInfoCas.get(
            manager_id=manager_id,
            portfolio_id=portfolio_trade.id,
        ).delete()
    except Exception:
        db.session.rollback()
        current_app.logger.error(f'[delete portfolio] failed! (err){traceback.format_exc()}')
        raise LogicError('删除组合失败！')


def get_portfolio_infos(manager_id):
    cas.init_conn()
    infos = ProductionInfoCas.filter(manager_id=manager_id)
    return [info.to_dict() for info in infos]


def daily_update_portfolio_infos():
    cas.init_conn()
    portfolio_trades = PortfolioTrade.filter_by_query().all()
    for portfolio_trade in portfolio_trades:
        current_app.logger.info(f'[update portfolio info] (id){portfolio_trade.id} (name){portfolio_trade.portfolio_name}')
        trade_history = TradeHistoryValidation(trade_history=portfolio_trade.trade_history).dict()['trade_history']
        portfolio_info = calc_portfolio_info(trade_history, portfolio_trade.benchmark_id_info)
        ProductionInfoCas.update_info(portfolio_trade, portfolio_info, datetime.datetime.now())

