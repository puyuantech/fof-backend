
import datetime

from pydantic import conlist
from typing_extensions import Literal

from bases.validation import BaseValidation


class RetValidation(BaseValidation):
    asset_list: conlist(str, min_items=1)


class CorrValidation(RetValidation):
    period: Literal['week','month']


class RecentValidation(BaseValidation):
    year: int = None


class DateValidation(BaseValidation):
    begin_date: datetime.date = None
    end_date: datetime.date = None


class TimeValidation(DateValidation):
    time_para: Literal['ALL','1M','3M','6M','1Y','YTD'] = None


class ProductRetValidation(BaseValidation):
    product_list: conlist(str, min_items=1)

