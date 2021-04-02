
from flask import g

from bases.validation import InvestorValidation
from bases.viewhandler import ApiViewHandler
from models import FOFNotification
from utils.decorators import login_required

from .libs import get_customers


class CustomerListAPI(ApiViewHandler):

    @login_required
    def get(self):
        return get_customers(g.token.manager_id)


class CustomerNotificationAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = InvestorValidation.get_valid_data(self.input)
        return FOFNotification.get_investor_notifications(g.token.manager_id, **data)

