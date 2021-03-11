import uuid
import datetime

from bases.dbwrapper import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash


class SuperAdmin(BaseModel):
    """
    超级管理员
    """
    __tablename__ = 'super_admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(256), nullable=False)
    last_login = db.Column(db.DATETIME, default=datetime.datetime.now)

    def to_dict(self, fields_list=None, remove_fields_list=None, remove_deleted=True):
        return super().to_dict(remove_fields_list=['password_hash'])

    @property
    def password(self):
        raise AttributeError("当前属性不可读")  # _password

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class SuperToken(BaseModel):
    """
    超级管理员token
    """
    __tablename__ = "super_token"

    id = db.Column(db.Integer, primary_key=True)                    # 编号
    key = db.Column(db.String(32))                                  # key值
    refresh_key = db.Column(db.String(32))                          # 刷新key值
    expires_at = db.Column(db.DateTime, nullable=False)             # 过期时间
    admin_id = db.Column(db.Integer, db.ForeignKey('super_admin.id'))
    super_admin = db.relationship('SuperAdmin', backref='super_token')

    @staticmethod
    def generate_key():
        return uuid.uuid4().hex

    @staticmethod
    def generate_expires_at():
        return datetime.datetime.now() + datetime.timedelta(minutes=60 * 24 * 30)

    def is_valid(self):
        return datetime.datetime.now() < self.expires_at

    def refresh(self, refresh_key):
        if self.refresh_key == refresh_key:
            self.key = self.generate_key()
            self.expires_at = self.generate_expires_at()

    @classmethod
    def generate_token(cls, admin_id):
        tokens = cls.filter_by_query(
            admin_id=admin_id,
        ).order_by(cls.expires_at.asc()).all()

        if len(tokens) < 5:
            token = cls.create(
                key=cls.generate_key(),
                refresh_key=cls.generate_key(),
                expires_at=cls.generate_expires_at(),
                admin_id=admin_id,
            )
        else:
            token = tokens[0]
            token.refresh(token.refresh_key)
            token.save()

        token = cls.get_by_id(token.id)
        return token

