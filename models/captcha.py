import datetime
from bases.dbwrapper import db, BaseModel
from bases.constants import IMG_CAPTCHA_EXPIRATION_IN_MINUTES
from bases.constants import MOBILE_CODE_EXPIRE_TIME


class CaptchaCode(BaseModel):
    __tablename__ = 'captcha_img'

    id = db.Column(db.Integer, primary_key=True)         # 编号
    key = db.Column(db.CHAR(64), default='')             # 缓存键
    value = db.Column(db.CHAR(64), default='')           # 验证码
    expires_at = db.Column(db.DATETIME, nullable=False)  # 过期时间

    @classmethod
    def generate_expires_at(cls):
        return datetime.datetime.now() + datetime.timedelta(minutes=IMG_CAPTCHA_EXPIRATION_IN_MINUTES)

    def is_valid(self, code):
        return self.value.lower() == code.lower() and datetime.datetime.now() < self.expires_at


class MobileCode(BaseModel):
    __tablename__ = 'mobile_code'

    id = db.Column(db.Integer, primary_key=True)         # 编号

    mobile = db.Column(db.CHAR(11), default='')          # 手机号
    value = db.Column(db.CHAR(64), default='')           # 验证码
    action = db.Column(db.CHAR(31))                      # 用途
    try_times = db.Column(db.Integer, default=0)         # 尝试次数
    success_times = db.Column(db.Integer, default=0)     # 成功次数
    expires_at = db.Column(db.DATETIME, nullable=False)  # 过期时间

    @classmethod
    def generate_expires_at(cls):
        return datetime.datetime.now() + datetime.timedelta(minutes=MOBILE_CODE_EXPIRE_TIME)

    def is_valid(self, code):
        return self.value.lower() == code.lower() and datetime.datetime.now() < self.expires_at

