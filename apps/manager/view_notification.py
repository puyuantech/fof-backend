
from flask import g

from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required

from .libs import get_notification_statistics, save_notification
from .validators.notification import NotificationValidation


class NotificationAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = NotificationValidation.get_valid_data(self.input)
        save_notification(manager_id=g.token.manager_id, **data)
        return 'success'


class NotificationStatisticsAPI(ApiViewHandler):

    @login_required
    def get(self):
        return get_notification_statistics(g.token.manager_id)

