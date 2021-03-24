from bases.dbwrapper import db, BaseModel
from bases.base_enmu import EnumBase


class MessageTask(BaseModel):
    """
    消息任务
    """
    __tablename__ = 'message_task'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)            # 编号
    manager_id = db.Column(db.String(32))
    fof_id = db.Column(db.String(63))
    name = db.Column(db.String(127))


class MessageTaskSub(BaseModel):
    """
    任务详情
    """
    class TaskType(EnumBase):
        MAIL = 1
        MOBILE = 2
        WE_CHAT = 3

    class TaskStatus(EnumBase):
        SUCCESS = 1
        FAILED = 2
        PENDING = 3

    __tablename__ = 'message_task_sub'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)            # 编号
    task_id = db.Column(db.Integer, db.ForeignKey('message_task.id'))
    task = db.relationship('MessageTask', backref='sub')
    manager_id = db.Column(db.String(32))
    name = db.Column(db.String(127))
    task_type = db.Column(db.Integer, nullable=False)                           # 消息类型
    task_content = db.Column(db.TEXT)                                           # 消息内容
    task_status = db.Column(db.Integer, default=TaskStatus.PENDING)
    err_msg = db.Column(db.String(255))
