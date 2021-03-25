
import datetime

from pydantic import conlist
from typing_extensions import Literal

from bases.validation import BaseValidation


class YearValidation(BaseValidation):
    year: int = None


class DateValidation(BaseValidation):
    begin_date: datetime.date = None
    end_date: datetime.date = None


class TimeValidation(DateValidation):
    time_para: Literal['ALL','1M','3M','6M','1Y','YTD'] = None


class AssetRetValidation(TimeValidation):
    asset_list: conlist(str, min_items=1)


class AssetRecentValidation(YearValidation):
    asset_list: conlist(str, min_items=1)


class IndustryRetValidation(TimeValidation):
    industry_list: conlist(str, min_items=1)


class IndustryRecentValidation(YearValidation):
    industry_list: conlist(str, min_items=1)


class ProductRetValidation(TimeValidation):
    product_list: conlist(str, min_items=1)


class ProductRecentValidation(YearValidation):
    product_list: conlist(str, min_items=1)


class ProductCorrValidation(ProductRetValidation):
    period: Literal['week','month']

