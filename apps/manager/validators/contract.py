
from pydantic import constr

from bases.validation import BaseValidation


class FOFStartValidation(BaseValidation):
    fof_id: constr(min_length=1)

