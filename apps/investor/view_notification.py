
from flask import g

from bases.constants import FOFNotificationType
from bases.globals import db
from bases.viewhandler import ApiViewHandler
from models import FOFNotification, NotificationActive
from utils.decorators import login_required

from .validators.notification import NotificationTypeValidation


class NotificationMenuAPI(ApiViewHandler):

    @login_required
    def get(self):
        unread_counts = FOFNotification.get_investor_unread_counts(g.token.manager_id, g.token.investor_id)

        notifications = {}
        for notification_type in FOFNotificationType.get_codes():
            latest_notification = FOFNotification.filter_by_query(
                notification_type=notification_type,
                manager_id=g.token.manager_id,
                investor_id=g.token.investor_id,
            ).order_by(
                FOFNotification.id.desc(),
            ).first()
            notifications[notification_type] = {
                'unread_count': unread_counts.get(notification_type, 0),
                'latest_notification': latest_notification and latest_notification.to_dict(),
            }

        NotificationActive.save_active_investor(g.token.manager_id, g.token.investor_id)
        return notifications


class NotificationListAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = NotificationTypeValidation.get_valid_data(self.input)
        notifications = FOFNotification.filter_by_query(
            **data,
            manager_id=g.token.manager_id,
            investor_id=g.token.investor_id,
        ).all()
        return [notification.to_dict() for notification in notifications]


class NotificationReadListAPI(ApiViewHandler):

    @login_required
    def put(self):
        data = NotificationTypeValidation.get_valid_data(self.input)
        notifications = FOFNotification.filter_by_query(
            **data,
            manager_id=g.token.manager_id,
            investor_id=g.token.investor_id,
            read=False,
        ).all()
        for notification in notifications:
            notification.update(commit=False, read=True)
        db.session.commit()
        return 'success'

