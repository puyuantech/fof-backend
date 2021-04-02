
from typing_extensions import Literal

from bases.validation import BaseValidation


class NotificationTypeValidation(BaseValidation):
    notification_type: Literal['nav_update','product_news','market_news','roadshow_info','system_news']

