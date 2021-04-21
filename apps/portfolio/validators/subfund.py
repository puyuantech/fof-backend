
import datetime

from pydantic import constr

from . import PortfolioIdValidation, PortfolioWithTimeValidation


class FundRetValidation(PortfolioWithTimeValidation):
    index_id: constr(min_length=1)


class FundPosValidation(PortfolioIdValidation):
    fund_id: constr(min_length=8, max_length=8)
    index_id: constr(min_length=1)


class RetResolveValidation(PortfolioIdValidation):
    begin_date: datetime.date
    end_date: datetime.date

