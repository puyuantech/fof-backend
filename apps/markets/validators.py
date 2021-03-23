
from bases.validation import BaseValidation


class RetValidation(BaseValidation):
    asset_list: conlist(str, min_items=1)


class RecentValidation(BaseValidation):
    year: int = None

