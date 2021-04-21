
from pydantic import constr
from typing_extensions import Literal

from . import PortfolioIdValidation


class RollingValidation(PortfolioIdValidation):
    index_id: constr(min_length=1)
    period: Literal['日度','周度','月度']
    windows: Literal[10,20,30,60,180,365]

