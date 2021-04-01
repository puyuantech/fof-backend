
from typing_extensions import Literal

from bases.validation import BaseValidation, UnitValidation


class NotificationTypeValidation(UnitValidation):
    notification_type: Literal['nav_update','product_news','market_news','roadshow_info','system_news']


class NotificationIDValidation(BaseValidation):
    notification_id: int

