import uuid
import datetime
import traceback

from flask import current_app
from bases.base_enmu import EnumBase
from bases.globals import settings
from bases.exceptions import VerifyError
from bases.dbwrapper import BaseModel, db
from utils.helper import generate_hash_char
from werkzeug.security import generate_password_hash, check_password_hash


TOKEN_EXPIRATION_IN_MINUTES = settings.get('TOKEN_EXPIRATION_IN_MINUTES', 60 * 24 * 30)
TOKEN_MAX_NUM = settings.get('TOKEN_MAX_NUM', 10)


class User(BaseModel):
    """
    用户
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(20), unique=True)
    username = db.Column(db.String(20))
    role_id = db.Column(db.Integer, default=0)                      # role_id 是否是管理员或者其他权限  1 管理员用户
    is_staff = db.Column(db.BOOLEAN, default=False)                 # 是否是员工
    staff_name = db.Column(db.String(20))                           # 员工姓名
    is_wx = db.Column(db.BOOLEAN, default=False)                    # 是否微信虚拟账号
    password_hash = db.Column(db.String(256), nullable=False)
    last_login = db.Column(db.DATETIME, default=datetime.datetime.now)
    last_login_investor = db.Column(db.String(32))

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

    @classmethod
    def create_main_user_investor(cls, mobile):
        user = cls.create(
            mobile=mobile,
            password='',
        )
        try:
            investor_id = generate_hash_char(user.id)
            investor = InvestorInfo(
                investor_id=investor_id,
                mobile_phone=mobile,
            )
            investor_map = UserInvestorMap(
                user_id=user.id,
                investor_id=investor_id,
                map_type=UserInvestorMap.MapType.MAIN,
            )
            db.session.add(investor_map)
            db.session.add(investor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            user.delete()
            current_app.logger.error(traceback.format_exc())
            raise VerifyError('创建用户失败！')

        return user, investor

    @classmethod
    def create_investor_sub_user(cls, user_id, investor_id):
        investor_map = UserInvestorMap.create(
            user_id=user_id,
            investor_id=investor_id,
            map_type=UserInvestorMap.MapType.SUB,
        )
        return investor_map

    def get_main_investor(self):
        investor = db.session.query(InvestorInfo).filter(
            UserInvestorMap.user_id == self.id,
            UserInvestorMap.investor_id == InvestorInfo.investor_id,
            UserInvestorMap.map_type == UserInvestorMap.MapType.MAIN,
        ).first()
        return investor


class UserInvestorMap(BaseModel):
    """
    用户 投资者 映射表
    """
    __tablename__ = 'user_investor_map'

    class MapType(EnumBase):
        MAIN = 1
        SUB = 2

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    investor_id = db.Column(db.String(32), nullable=False)
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
    mobile_phone = db.Column(db.String(20), unique=True)  # 手机
    landline_phone = db.Column(db.String(20))  # 座机
    profession = db.Column(db.String(32))  # 职业
    job = db.Column(db.String(32))  # 职务
    postcode = db.Column(db.String(20))  # 邮编
    address = db.Column(db.String(256))  # 住址

    def create_manager_map(self, manager_id, mobile=None):
        unit_map = UnitMap.create(
            investor_id=self.investor_id,
            manager_id=manager_id,
            mobile=mobile,
        )
        return unit_map

    def check_manager_map(self, manager_id):
        unit_map = UnitMap.filter_by_query(
            investor_id=self.investor_id,
            manager_id=manager_id,
        ).first()
        return unit_map

    def update_columns(self, request):
        columns = [
            'name',
            'email',
            'nationality',
            'gender',
            'age',
            'landline_phone',
            'profession',
            'job',
            'postcode',
            'address',
        ]

        for i in columns:
            if request.json.get(i) is not None:
                self.update(commit=False, **{i: request.json.get(i)})
        self.save()
        return self

    @classmethod
    def get_by_mobile(cls, mobile):
        return cls.filter_by_query(
            mobile_phone=mobile,
        ).first()


class UnitMap(BaseModel):
    """
    投资者和管理者关联表
    """
    __tablename__ = 'user_unit_map'

    class InvestorType(EnumBase):
        NATURAL = 1
        INSTITUTION = 2
        PRODUCTION = 3

    class CredType(EnumBase):
        身份证 = 1
        港澳通行证 = 2
        护照 = 3
        军官证 = 4

    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.String(32), db.ForeignKey('user_manager_info.manager_id'), nullable=False)
    investor_id = db.Column(db.String(32), db.ForeignKey('user_investor_info.investor_id'), nullable=False)
    investor_type = db.Column(db.Integer, default=1)                    # 投资者类型
    name = db.Column(db.String(20))                                     # 姓名
    cred_type = db.Column(db.String(20))                                # 证件类型 1身份证 2护照
    cred = db.Column(db.String(64))                                     # 证件编号
    mobile = db.Column(db.String(20))                                   # 手机号
    amount = db.Column(db.Float)                                        # 投资总额
    email = db.Column(db.String(64))                                    # 邮件地址
    sign_date = db.Column(db.String(20))                                # 签约日期
    address = db.Column(db.String(256))                                 # 通讯地址
    origin = db.Column(db.String(20))                                   # 来源
    status = db.Column(db.Integer)                                      # 客户审核状态
    sponsor = db.Column(db.String(20))                                  # 推荐人
    salesman = db.Column(db.String(20))                                 # 销售人员
    latest_time = db.Column(db.DATETIME)                                # 最后操作时间

    def update_columns(self, request):
        columns = [
            'investor_type',
            'name',
            'cred_type',
            'cred',
            'amount',
            'email',
            'sign_date',
            'address',
            'origin',
            'status',
            'salesman',
        ]

        for i in columns:
            if request.json.get(i) is not None:
                self.update(commit=False, **{i: request.json.get(i)})
        self.save()
        return self


class ManagerInfo(BaseModel):
    """
    管理者
    """
    __tablename__ = 'user_manager_info'

    class IDType(EnumBase):
        备案证明 = 1
        组织机构代码 = 2
        社会统一信用代码 = 3
        工商注册号 = 4
        其他证件 = 5

    manager_id = db.Column(db.String(32), primary_key=True)         # 代码
    name = db.Column(db.String(127))                                # 名称
    email = db.Column(db.String(127), unique=True)                  # 邮箱
    mobile = db.Column(db.String(11))                               # 手机号
    id_type = db.Column(db.Integer)                                 # 凭证类型
    id_number = db.Column(db.String(127))                           # 凭证编码
    address = db.Column(db.String(255))                             # 地址
    legal_person = db.Column(db.String(31))                         # 法人
    logo = db.Column(db.String(255))                                # Logo


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

    @classmethod
    def clear(cls, user_id):
        cls.filter_by_query(
            show_deleted=True,
            user_id=user_id,
        ).delete()

    def refresh(self, refresh_key):
        if self.refresh_key == refresh_key:
            print(self.refresh_key)
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
