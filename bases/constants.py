from bases.base_enmu import EnumBase

# 图片验证码过期时间
IMG_CAPTCHA_EXPIRATION_IN_MINUTES = 5
MOBILE_CODE_EXPIRE_TIME = 5
RISK_LEVEL_EXPIRE_DAY = 365 * 3


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


class CertificationStatus(EnumBase):
    # UNVERIFIED = 'unverified'
    VERIFYING = 'verifying'
    # VERIFY_FAILED = 'verify_failed'
    REVIEWING = 'reviewing'
    REVIEW_FAILED = 'review_failed'
    REVIEW_SUCCESSFUL = 'review_successful'


class ContractStatus(EnumBase):
    # UNBOOKED = 'unbooked'
    BOOKED = 'booked'
    SIGNING = 'signing'
    SIGNED = 'signed'


class UserRiskLevel(EnumBase):
    保守型 = 'C1'
    稳健型 = 'C2'
    平衡型 = 'C3'
    成长型 = 'C4'
    进取型 = 'C5'


class UserRiskLevelExplanation(EnumBase):
    保守型 = '建议您更多的进行保守型投资，可考虑投资于保守型产品'
    稳健型 = '您的投资风格较为稳健，考虑投资于固定收益类产品'
    平衡型 = '您的风险意识很高，但同时也期望有一定的增值能力'
    成长型 = '您期望获得较高收益，同时也能接受资产的波动性，可考虑进行证券等组合投资'
    进取型 = '您已充分了解高风险高收益的信息，可考虑进行PE类等高回报性的投资'

