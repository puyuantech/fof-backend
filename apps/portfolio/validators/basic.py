
from pydantic import constr

from . import PortfolioIdValidation, PortfolioWithTimeValidation


class PortfolioNavValidation(PortfolioWithTimeValidation):
    index_id: constr(min_length=1)


class PortfolioStatsValidation(PortfolioIdValidation):
    index_id: constr(min_length=1)

