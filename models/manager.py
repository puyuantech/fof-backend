
from bases.dbwrapper import db, BaseModel


class ManagerSecret(BaseModel):
    """管理者签约密钥"""
    __tablename__ = 'manager_secret'

    manager_id = db.Column(db.String(32), primary_key=True)

    user_id = db.Column(db.Integer)
    secret = db.Column(db.String(128))


class ManagerWeChatAccount(BaseModel):
    """管理者微信公众号账户"""
    __tablename__ = 'manager_wx_account'

    manager_id = db.Column(db.String(32), primary_key=True)

    app_id = db.Column(db.String(127))
    app_sec = db.Column(db.String(127))
    token = db.Column(db.String(127))
