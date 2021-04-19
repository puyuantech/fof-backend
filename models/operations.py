from bases.dbwrapper import db, BaseModel
from sqlalchemy.dialects.mysql import DOUBLE


class Operation(BaseModel):
    """
    管理者操作记录
    """
    __tablename__ = 'operations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)            # 编号
    user_id = db.Column(db.Integer)                                             #
    investor_id = db.Column(db.String(32))                                      # 投资者ID
    ip = db.Column(db.String(31))                                               # IP
    action = db.Column(db.String(31))                                           # 操作
    url = db.Column(db.TEXT)                                                    # 请求地址
    method = db.Column(db.String(15))                                           # 请求方法
    request_data = db.Column(db.TEXT)                                           # 请求体
    response_data = db.Column(db.TEXT)                                          # 返回数据
    response_status = db.Column(db.Integer)                                     # 返回状态码
    manager_id = db.Column(db.String(32))                                       # 管理者ID


class InvestorOperation(BaseModel):
    """
    投资者操作记录
    """
    __tablename__ = 'operations_investor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)            # 编号
    user_id = db.Column(db.Integer)                                             #
    investor_id = db.Column(db.String(32))                                      # 投资者ID
    ip = db.Column(db.String(31))                                               # IP
    action = db.Column(db.String(31))                                           # 操作
    url = db.Column(db.TEXT)                                                    # 请求地址
    method = db.Column(db.String(15))                                           # 请求方法
    request_data = db.Column(db.TEXT)                                           # 请求体
    response_data = db.Column(db.TEXT)                                          # 返回数据
    response_status = db.Column(db.Integer)                                     # 返回状态码
    manager_id = db.Column(db.String(32))                                       # 管理者ID


class CeleryTaskLogs(BaseModel):
    """
    Celery 任务记录
    """
    __tablename__ = 'celery_task_logs'

    success_status = 1
    fail_status = 0

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(128))
    task_id = db.Column(db.String(64), index=True, unique=True)
    retval = db.Column(db.Text)
    done = db.Column(db.Boolean)
    task_status = db.Column(db.Boolean)
    exc = db.Column(db.Text)
    einfo = db.Column(db.Text)
    args = db.Column(db.Text)
    kwargs = db.Column(db.Text)
    available = db.Column(db.Boolean, default=1)
    time_done = db.Column(db.DateTime)
