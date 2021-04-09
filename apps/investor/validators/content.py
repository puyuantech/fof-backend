
from typing_extensions import Literal

from bases.validation import BaseValidation


class ContentStatisticsValidation(BaseValidation):
    info_id: int
    info_type: Literal[1, 2, 3, 4, 5, 6]

