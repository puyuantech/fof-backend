
from bases.dbwrapper import db, BaseModel


class ManagerWeChatAccount(BaseModel):
    """管理者微信公众号账户"""
    __tablename__ = 'manager_wx_account'

    manager_id = db.Column(db.String(32), primary_key=True)

    app_id = db.Column(db.String(127))
    app_sec = db.Column(db.String(127))
    token = db.Column(db.String(127))
    encoding_aes_key = db.Column(db.String(127))
    nav_template_id = db.Column(db.String(127))


class ManagerEmailAccount(BaseModel):
    """管理者邮箱转发设置"""
    __tablename__ = 'manager_email_account'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manager_id = db.Column(db.String(32), unique=True)

    server = db.Column(db.String(127))                      # 邮箱服务器
    port = db.Column(db.Integer)                            # 端口
    is_ssl = db.Column(db.BOOLEAN, default=True)            # 是否使用ssl
    username = db.Column(db.String(63))                     # 账号名称
    secret = db.Column(db.String(63))                       # 授权码
    sender = db.Column(db.String(127))                      # 机构名称


class ManagerNavEmail(BaseModel):
    """管理者净值接收邮箱"""
    __tablename__ = 'manager_nav_email'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manager_id = db.Column(db.String(32), unique=True)

    server = db.Column(db.String(127))                      # 邮箱服务器
    port = db.Column(db.Integer)                            # 端口
    email = db.Column(db.String(127), unique=True)          # 邮箱
    password = db.Column(db.String(63))                     # 邮箱密码
