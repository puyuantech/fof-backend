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
    UNBOOKED = 'unbooked'
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


class ContractTemplateType(EnumBase):
    风险揭示书 = 'risk_disclose'
    基金合同 = 'fund_contract'
    补充协议 = 'protocol'
    风险告知书 = 'fund_matching'
    回访确认书 = 'lookback'


class HaiFengTemplateType(EnumBase):
    fund_contract = 0 # 基金合同
    # '托管协议' = 1
    # '代销合同' = 2
    protocol = 3 # 补充协议
    # '征询意见函' = 4
    # '公告告知' = 5
    risk_disclose = 6 # 风险揭示书
    # '其他预留' = 7
    # '有限合伙协议' = 21
    # '基金运营服务协议' = 22
    # '其他' = 99

    @classmethod
    def read(cls, code):
        cls._init_cache()
        return cls._code_2_name_cache.get(code)


class FOFNotificationType(EnumBase):
    NAV_UPDATE = 'nav_update'       # 净值更新
    PRODUCT_NEWS = 'product_news'   # 产品公告
    MARKET_NEWS = 'market_news'     # 专属资讯
    ROADSHOW_INFO = 'roadshow_info' # 路演信息
    SYSTEM_NEWS = 'system_news'     # 系统公告


class TemplateStatus(EnumBase):
    NOSTART = 'no_start'      # 未开始
    PROCESSING = 'processing' # 处理中
    SIGNING = 'signing'       # 待签署
    COMPLETED = 'completed'   # 已完成


class HaiFengCertType(EnumBase):
    身份证 = 1
    社保卡 = 2
    护照 = 3
    军官证 = 4
    港澳通行证 = 5
    台胞证 = 6
    其他证件 = 7

