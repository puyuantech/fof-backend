
from typing_extensions import Literal

from . import TradeWithTimeValidation


class RetDistributionValidation(TradeWithTimeValidation):
    period: Literal['1W','1M','3M']

