
import datetime

from pydantic import conlist
from typing_extensions import Literal

from bases.validation import BaseValidation


class YearValidation(BaseValidation):
    year: int = None


class TimeValidation(BaseValidation):
    begin_date: datetime.date = None
    end_date: datetime.date = None
    time_para: Literal['ALL','1W','1M','3M','6M','1Y','YTD'] = None


class AssetRetValidation(TimeValidation):
    asset_list: conlist(str, min_items=1)


class AssetRecentValidation(YearValidation):
    weekly: bool = False
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


class ValuationTimeValidation(BaseValidation):
    begin_date: datetime.date = None
    end_date: datetime.date = None
    time_para: Literal['ALL','1Y','2Y','3Y','5Y','YTD'] = None


class ValuationIndexValidation(ValuationTimeValidation):
    index_list: conlist(str, min_items=1)
    valuation_type: str # PB, PE, ROE


class ValuationHistoryValidation(ValuationTimeValidation):
    index_id: str
    valuation_type: str # PB, PE, ROE


class StockDebtValidation(BaseValidation):
    index_id: str
    valuation_type: str
    debt_ret_index: str


class SideCapValidation(TimeValidation):
    direction: Literal['北向资金','南向资金']
    index_id: str


class AHPremValidation(TimeValidation):
    frequency: Literal['1D','1W','1M']

