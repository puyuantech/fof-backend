
from typing_extensions import Literal

from . import PortfolioWithTimeValidation


class RetDistributionValidation(PortfolioWithTimeValidation):
    period: Literal['1W','1M','3M']

