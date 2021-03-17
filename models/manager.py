
from bases.dbwrapper import db, BaseModel


class ManagerSecret(BaseModel):
    """管理者签约密钥"""
    __tablename__ = 'manager_secret'

    manager_id = db.Column(db.String(32), primary_key=True)

    user_id = db.Column(db.Integer)
    secret = db.Column(db.String(128))

