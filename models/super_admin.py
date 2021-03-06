import uuid
import datetime

from bases.dbwrapper import BaseModel, db
from bases.base_enmu import EnumBase
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


class ApplyFile(BaseModel):
    """
    申请材料
    """
    __tablename__ = "admin_apply_file"

    class SignEnum(EnumBase):
        PENDING = 0
        FAILED = 1
        SUCCESS = 2

    id = db.Column(db.Integer, primary_key=True)                        # 编号
    rand_str = db.Column(db.String(127))                                # 随机编码
    email = db.Column(db.String(63))                                    # 邮箱
    mobile = db.Column(db.String(11))                                   # 手机号
    manager_name = db.Column(db.String(127))                            # 机构名称
    manager_id = db.Column(db.String(31))                               # 机构ID
    manager_cred_type = db.Column(db.String(31))                        # 证件类型
    manager_cred_file = db.Column(db.String(127))                       # 证件url
    manager_cred_no = db.Column(db.String(127))                         # 证件号码
    manager_bank_card_no = db.Column(db.String(127))                    # 对公账户卡号
    manager_bank_short_name = db.Column(db.String(127))                 # 对公帐号开户行简称
    legal_person = db.Column(db.String(31))                             # 法人
    lp_cred_type = db.Column(db.String(31))                             # 法人证件类型
    lp_cred_file = db.Column(db.String(127))                            # 法人证件文件
    lp_cred_no = db.Column(db.String(127))                              # 法人证件号码
    authorization_file = db.Column(db.String(127))                      # 授权文件
    service_file = db.Column(db.String(127))                            # 服务协议
    pu_yuan_auth_file = db.Column(db.String(127))                       # 璞元授权文件
    admin_name = db.Column(db.String(15))                               # 签约人姓名
    admin_cred_no = db.Column(db.String(63))                            # 签约人证件号码
    admin_cred_type = db.Column(db.String(31))                          # 签约人证件类型
    admin_cred_file = db.Column(db.String(127))                         # 签约人证件文件
    sign_stage = db.Column(db.Integer, default=1)                       # 提交阶段  1 ｜ 2


class ApplyStatus(BaseModel):
    """
    申请状态
    """
    __tablename__ = "admin_apply_status"

    class SignEnum(EnumBase):
        PENDING = 0
        FAILED = 1
        SUCCESS = 2

    id = db.Column(db.Integer, primary_key=True)                        # 编号
    apply_id = db.Column(db.Integer, db.ForeignKey('admin_apply_file.id'))
    file = db.relationship('ApplyFile', backref='status')
    manager_cred = db.Column(db.BOOLEAN, default=False)
    lp_cred = db.Column(db.BOOLEAN, default=False)
    admin_cred = db.Column(db.BOOLEAN, default=False)
    service_cred = db.Column(db.BOOLEAN, default=False)
    hf_success = db.Column(db.BOOLEAN, default=False)
    sign_status = db.Column(db.Integer)                                 # 审核状态
    failed_reason = db.Column(db.String(127))                           # 失败原因

