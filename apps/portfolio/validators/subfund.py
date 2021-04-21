
import datetime

from pydantic import constr

from . import TradeHistoryValidation, TradeWithTimeValidation


class FundAlphaValidation(TradeHistoryValidation):
    benchmark_id_info: dict


class FundRetValidation(TradeWithTimeValidation):
    benchmark_id_info: dict
    index_id: constr(min_length=1)


class FundPosValidation(TradeHistoryValidation):
    fund_id: constr(min_length=8, max_length=8)
    index_id: constr(min_length=1)


class RetResolveValidation(TradeHistoryValidation):
    begin_date: datetime.date
    end_date: datetime.date

