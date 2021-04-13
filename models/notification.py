
import datetime

from sqlalchemy import distinct, func

from bases.constants import FOFNotificationType
from bases.dbwrapper import db, BaseModel
from utils.helper import parse_date_counts

from .information import InfoStatistics


class FOFNotification(BaseModel):
    """
    消息中心
    """
    __tablename__ = 'fof_notification'

    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.String(32))        # 发送者
    investor_id = db.Column(db.String(32))       # 接收者
    notification_type = db.Column(db.String(16)) # 消息类型
    content_id = db.Column(db.Integer)           # 资讯ID, 净值更新定为 -1
    content = db.Column(db.JSON)                 # 资讯内容
    read = db.Column(db.BOOLEAN, default=False)  # 是否已读

    def to_dict(self, fields_list=None, remove_fields_list=None, remove_deleted=True):
        data = super().to_dict(fields_list, remove_fields_list, remove_deleted)
        if data['notification_type'] == FOFNotificationType.ROADSHOW_INFO:
            data['content']['viewed'] = InfoStatistics.get_user_count(data['content_id'])
        return data

    @classmethod
    def send_nav_update(cls, manager_id, investor_id, content: dict):
        cls.create(
            manager_id=manager_id,
            investor_id=investor_id,
            notification_type=FOFNotificationType.NAV_UPDATE,
            content_id=-1,
            content=content,
        )

    @classmethod
    def get_notification_counts(cls, manager_id, start_time, filter_read=False):
        filter_condition = {'manager_id': manager_id}
        if filter_read:
            filter_condition['read'] = True

        date_counts = db.session.query(
            func.date(cls.create_time),
            func.count(cls.id),
        ).filter_by(
            **filter_condition,
        ).filter(
            cls.create_time > start_time,
        ).group_by(
            func.date(cls.create_time),
        ).all()

        dates, counts = parse_date_counts(date_counts)
        return {
            'dates': dates,
            'counts': counts,
            'total': sum(counts),
        }

    @classmethod
    def get_manager_content_ids(cls, manager_id):
        content_ids = db.session.query(
            distinct(cls.content_id),
        ).filter_by(
            manager_id=manager_id,
        ).all()
        return set(content_id for content_id, in content_ids)

    @classmethod
    def get_investor_counts(cls, manager_id):
        counts = db.session.query(
            cls.investor_id,
            cls.read,
            func.count(cls.id),
        ).filter_by(
            manager_id=manager_id,
        ).group_by(
            cls.investor_id,
            cls.read,
        ).all()

        investor_counts = {}
        for investor_id, read, count in counts:
            investor_counts.setdefault(investor_id, {})[read] = count
        return investor_counts

    @classmethod
    def get_investor_notifications(cls, manager_id, investor_id):
        notifications = cls.filter_by_query(
            manager_id=manager_id,
            investor_id=investor_id,
        ).all()
        return [notification.to_dict() for notification in notifications]

    @classmethod
    def get_investor_unread_counts(cls, manager_id, investor_id):
        unread_counts = db.session.query(
            cls.notification_type,
            func.count(cls.id),
        ).filter_by(
            manager_id=manager_id,
            investor_id=investor_id,
            read=False,
            is_deleted=False,
        ).group_by(
            cls.notification_type,
        ).all()
        return {notification_type: unread_count for notification_type, unread_count in unread_counts}


class NotificationActive(BaseModel):
    """
    消息中心活跃用户
    """
    __tablename__ = 'notification_active'

    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.String(32))
    investor_id = db.Column(db.String(32))
    date = db.Column(db.Date)

    @classmethod
    def save_active_investor(cls, manager_id, investor_id):
        date = str(datetime.datetime.now().date())

        active = cls.filter_by_query(
            manager_id=manager_id,
            investor_id=investor_id,
            date=date,
        ).one_or_none()

        if not active:
            cls.create(
                manager_id=manager_id,
                investor_id=investor_id,
                date=date,
            )

    @classmethod
    def get_total_active_counts(cls, manager_id, start_date):
        return db.session.query(
            func.count(distinct(cls.id)),
        ).filter_by(
            manager_id=manager_id,
        ).filter(
            cls.date > start_date,
        ).scalar()

    @classmethod
    def get_active_counts(cls, manager_id, start_date):
        date_counts = db.session.query(
            cls.date,
            func.count(cls.id),
        ).filter_by(
            manager_id=manager_id,
        ).filter(
            cls.date > start_date,
        ).group_by(
            cls.date,
        ).all()

        dates, counts = parse_date_counts(date_counts)
        return {
            'dates': dates,
            'counts': counts,
            'total': cls.get_total_active_counts(manager_id, start_date),
        }

