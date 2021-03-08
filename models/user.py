import uuid
import datetime

from bases.globals import settings
from bases.dbwrapper import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash


TOKEN_EXPIRATION_IN_MINUTES = settings.get('TOKEN_EXPIRATION_IN_MINUTES', 60 * 24)
TOKEN_MAX_NUM = settings.get('TOKEN_MAX_NUM', 2)


class User(BaseModel):
    """
    用户
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(20))
    username = db.Column(db.String(20))
    role_id = db.Column(db.Integer, default=0)                      # role_id 是否是管理员或者其他权限  1 管理员用户
    is_staff = db.Column(db.BOOLEAN, default=False)                 # 是否是员工
    is_wx = db.Column(db.BOOLEAN, default=False)                    # 是否微信虚拟账号
    password_hash = db.Column(db.String(256), nullable=False)
    last_login = db.Column(db.DATETIME, default=datetime.datetime.now)
    last_login_investor = db.Column(db.String(32))

    investors = db.relationship(
        'InvestorInfo',
        secondary='user_investor_map',
        backref='users',
    )

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


class UserInvestorMap(BaseModel):
    """
    用户 投资者 映射表
    """
    __tablename__ = 'user_investor_map'
    map_type_choice = [
        (1, 'main'),
        (2, 'sub'),
    ]

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    investor_id = db.Column(db.String(32), db.ForeignKey('user_investor_info.investor_id'), nullable=False)
    map_type = db.Column(db.Integer)


class InvestorInfo(BaseModel):
    """
    投资者
    """
    __tablename__ = 'user_investor_info'

    investor_id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(10))  # 姓名
    email = db.Column(db.String(64))  # 邮箱
    nationality = db.Column(db.String(32))  # 国籍
    gender = db.Column(db.Integer, default=0)  # 性别(1: 男, 2: 女)
    age = db.Column(db.Integer)  # 年龄
    mobile_phone = db.Column(db.String(20))  # 手机
    landline_phone = db.Column(db.String(20))  # 座机
    profession = db.Column(db.String(32))  # 职业
    job = db.Column(db.String(32))  # 职务
    postcode = db.Column(db.String(20))  # 邮编
    address = db.Column(db.String(256))  # 住址


class UnitMap(BaseModel):
    """
    投资者和管理者关联表
    """
    __tablename__ = 'user_unit_map'

    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.String(32), db.ForeignKey('user_manager_info.manager_id'), nullable=False)
    investor_id = db.Column(db.String(32), db.ForeignKey('user_investor_info.investor_id'), nullable=False)
    name = db.Column(db.String(20))  # 姓名
    amount = db.Column(db.Float)  # 投资总额
    sign_date = db.Column(db.String(20))  # 签约日期
    sponsor = db.Column(db.String(20))  # 介绍人
    cred_type = db.Column(db.String(20))  # 证件类型 1身份证 2护照
    cred = db.Column(db.String(64))  # 证件编号
    is_institution = db.Column(db.BOOLEAN, default=False)  # 是否机构
    address = db.Column(db.String(256))  # 通讯地址
    ins_name = db.Column(db.String(63))  # 机构名称
    ins_code = db.Column(db.String(31))  # 机构代码
    contact_name = db.Column(db.String(31))  # 联系人
    contact_mobile = db.Column(db.String(20))  # 联系方式
    origin = db.Column(db.String(20))  # 来源
    status = db.Column(db.Integer)  # 客户状态
    salesman = db.Column(db.String(20))  # 销售人员


class ManagerInfo(BaseModel):
    """
    管理者
    """
    __tablename__ = 'user_manager_info'

    manager_id = db.Column(db.String(32), primary_key=True)         # 代码
    name = db.Column(db.String(127))                                # 名称
    id_type = db.Column(db.Integer)                                 # 凭证类型
    id_number = db.Column(db.String(127))                           # 凭证编码


class ManagerUserMap(BaseModel):
    """
    管理者 映射表
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    user_id = db.Column(db.Integer)
    manager_id = db.Column(db.String(32))


class Token(BaseModel):
    """
    用户token
    """
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True)      # 编号
    key = db.Column(db.String(32))                         # key值
    refresh_key = db.Column(db.String(32))                 # 刷新key值
    expires_at = db.Column(db.DateTime, nullable=False)  # 过期时间
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='token')
    manager_id = db.Column(db.String(32))
    investor_id = db.Column(db.String(32))

    @staticmethod
    def generate_key():
        return uuid.uuid4().hex

    @staticmethod
    def generate_expires_at():
        return datetime.datetime.now() + datetime.timedelta(minutes=TOKEN_EXPIRATION_IN_MINUTES)

    def is_valid(self):
        return datetime.datetime.now() < self.expires_at

    def refresh(self, refresh_key):
        if self.refresh_key == refresh_key:
            self.key = self.generate_key()
            self.manager_id = None
            self.investor_id = None
            self.expires_at = self.generate_expires_at()

    @classmethod
    def generate_token(cls, user_id):
        tokens = cls.filter_by_query(
            user_id=user_id,
        ).order_by(cls.expires_at.asc()).all()

        if len(tokens) < TOKEN_MAX_NUM:
            token = cls.create(
                key=cls.generate_key(),
                refresh_key=cls.generate_key(),
                expires_at=cls.generate_expires_at(),
                user_id=user_id,
            )
        else:
            token = tokens[0]
            token.refresh(token.refresh_key)
            token.save()

        token = cls.get_by_id(token.id)
        return token
