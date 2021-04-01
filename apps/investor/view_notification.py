
from bases.constants import FOFNotificationType
from bases.globals import db
from bases.viewhandler import ApiViewHandler
from models import FOFNotification
from utils.decorators import login_required

from .validators.notification import UnitValidation, NotificationTypeValidation, NotificationIDValidation


class NotificationMenuAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = UnitValidation.get_valid_data(self.input)
        unread_counts = FOFNotification.get_unread_counts(**data)

        notifications = {}
        for notification_type in FOFNotificationType.get_codes():
            latest_notification = FOFNotification.filter_by_query(**data, notification_type=notification_type).order_by(FOFNotification.id.desc()).one_or_none()
            notifications[notification_type] = {
                'unread_count': unread_counts.get(notification_type, 0),
                'latest_notification': latest_notification and latest_notification.to_dict(),
            }
        return notifications


class NotificationListAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = NotificationTypeValidation.get_valid_data(self.input)
        notifications = FOFNotification.filter_by_query(**data).all()
        return [notification.to_dict() for notification in notifications]


class NotificationReadAPI(ApiViewHandler):

    @login_required
    def put(self):
        # 待定
        data = NotificationIDValidation.get_valid_data(self.input)
        notification = FOFNotification.get_by_id(data['notification_id'])
        notification.update(read=True)
        return 'success'


class NotificationReadListAPI(ApiViewHandler):

    @login_required
    def put(self):
        data = NotificationTypeValidation.get_valid_data(self.input)
        notifications = FOFNotification.filter_by_query(**data, read=False).all()
        for notification in notifications:
            notification.update(commit=False, read=True)
        db.session.commit()
        return 'success'

