
import datetime

from pydantic import constr
from typing import List

from bases.validation import BaseValidation


class FundValidation(BaseValidation):
    fund_id: constr(min_length=8, max_length=8)
    weight: float
    fund_type: str


class TradeValidation(BaseValidation):
    datetime: datetime.date
    fund_weight: List[FundValidation]


class BenchmarkValidation(BaseValidation):
    asset_name: constr(min_length=1)
    index_name: constr(min_length=1)
    index_id: constr(min_length=1)
    weight: float


class TradeHistoryValidation(BaseValidation):
    trade_history: List[TradeValidation]


class PortfolioTradeValidation(TradeHistoryValidation):
    portfolio_name: constr(min_length=1, max_length=32)
    benchmark_info: List[BenchmarkValidation]


class PortfolioUpdateValidation(PortfolioTradeValidation):
    portfolio_id: int

