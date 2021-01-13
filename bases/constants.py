from bases.base_enmu import EnumBase

# 图片验证码过期时间
IMG_CAPTCHA_EXPIRATION_IN_MINUTES = 5
MOBILE_CODE_EXPIRE_TIME = 5


class SMS(EnumBase):
    LOGIN = 'SMS_203780299'


class StuffEnum(EnumBase):
    ADMIN = 1
    FUND_MANAGER = 2
    OPE_MANAGER = 3
    INVESTOR = 4


class ProductionStatus(EnumBase):
    RAISE = 'raise'
    OPEN = 'open'
    CLOSE = 'close'
    LIQUIDATE = 'liquidate'

