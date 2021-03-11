from bases.dbwrapper import db, BaseModel
from sqlalchemy.dialects.mysql import DOUBLE


class Operation(BaseModel):
    """
    用户操作记录
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
