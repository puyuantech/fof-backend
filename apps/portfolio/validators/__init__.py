
import datetime

from typing_extensions import Literal

from bases.validation import BaseValidation


class TimeValidation(BaseValidation):
    begin_date: datetime.date = None
    end_date: datetime.date = None
    time_para: Literal['ALL','1W','1M','3M','6M','1Y','YTD'] = None


class PortfolioIdValidation(BaseValidation):
    portfolio_id: int


class PortfolioWithTimeValidation(TimeValidation):
    portfolio_id: int

