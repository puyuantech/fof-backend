
from pydantic import conlist, constr, validator
from pydantic.validators import make_literal_validator
from typing_extensions import Literal

from bases.validation import BaseValidation


class ContentValidation(BaseValidation):
    content_type: Literal[1, 2, 4, 5, 6] # 资讯类型
    content_id: int                      # 资讯ID
    content: dict                        # 资讯内容


class NotificationValidation(BaseValidation):
    investor_ids: conlist(constr(max_length=32), min_items=1)
    contents: conlist(ContentValidation, min_items=1)


class StatisticsValidation(BaseValidation):
    days: int = 30

    @validator('days')
    def days_literal_validator(cls, v):
        return make_literal_validator(Literal[7, 30])(v)

