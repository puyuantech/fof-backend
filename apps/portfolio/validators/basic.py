
from pydantic import constr

from . import TradeHistoryValidation, TradeWithTimeValidation


class PortfolioNavValidation(TradeWithTimeValidation):
    index_id: constr(min_length=1)


class PortfolioStatsValidation(TradeHistoryValidation):
    index_id: constr(min_length=1)

