
import datetime

from pydantic import constr
from typing import List
from typing_extensions import Literal

from bases.validation import BaseValidation


class TimeValidation(BaseValidation):
    begin_date: datetime.date = None
    end_date: datetime.date = None
    time_para: Literal['ALL','1W','1M','3M','6M','1Y','YTD'] = None


class FundValidation(BaseValidation):
    fund_id: constr(min_length=8, max_length=8)
    weight: float
    fund_type: str


class TradeValidation(BaseValidation):
    datetime: datetime.date
    fund_weight: List[FundValidation]


class TradeHistoryValidation(BaseValidation):
    trade_history: List[TradeValidation]


class TradeWithTimeValidation(TimeValidation):
    trade_history: List[TradeValidation]

