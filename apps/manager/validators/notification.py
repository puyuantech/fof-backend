
from pydantic import conlist, constr
from typing_extensions import Literal

from bases.validation import BaseValidation


class NotificationValidation(BaseValidation):
    investor_ids: conlist(constr(max_length=32), min_items=1)
    manager_id: constr(max_length=32)
    notification_type: Literal['nav_update','product_news','market_news','roadshow_info','system_news']
    content: dict

