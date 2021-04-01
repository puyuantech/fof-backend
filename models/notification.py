
from sqlalchemy import func

from bases.dbwrapper import db, BaseModel


class FOFNotification(BaseModel):
    """
    消息中心
    """
    __tablename__ = 'fof_notification'

    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.String(32))        # 发送者
    investor_id = db.Column(db.String(32))       # 接收者
    notification_type = db.Column(db.String(16)) # 消息类型
    content = db.Column(db.JSON)                 # 内容ID、关联产品ID、摘要信息、摘要图片、作者、创建时间等
    read = db.Column(db.BOOLEAN, default=False)  # 是否已读

    @classmethod
    def get_unread_counts(cls, manager_id, investor_id):
        unread_counts = db.session.query(
            cls.notification_type,
            func.count(cls.id),
        ).filter_by(
            manager_id=manager_id,
            investor_id=investor_id,
            read=False,
        ).group_by(
            cls.notification_type
        ).all()
        return {notification_type: unread_count for notification_type, unread_count in unread_counts}

