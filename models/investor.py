import uuid

from bases.constants import CertificationStatus, ContractStatus
from bases.dbwrapper import db, BaseModel
from bases.exceptions import LogicError


class InvestorMixin:

    name = db.Column(db.String(10))           # 姓名
    email = db.Column(db.String(64))          # 邮箱
    nationality = db.Column(db.String(32))    # 国籍
    gender = db.Column(db.Integer, default=0) # 性别(1: 男, 2: 女)
    age = db.Column(db.Integer)               # 年龄
    mobile_phone = db.Column(db.String(20))   # 手机
    landline_phone = db.Column(db.String(20)) # 座机
    profession = db.Column(db.String(32))     # 职业
    job = db.Column(db.String(32))            # 职务
    postcode = db.Column(db.String(20))       # 邮编
    address = db.Column(db.String(256))       # 住址

    cert_type = db.Column(db.String(10))  # 证件类型
    cert_num = db.Column(db.String(32))   # 证件编号
    cert_expire_date = db.Column(db.Date) # 证件过期时间

    cert_front_image_url_key = db.Column(db.String(128)) # 证件正面照片
    cert_back_image_url_key = db.Column(db.String(128))  # 证件反面照片
    cert_image_time = db.Column(db.DateTime)             # 上传证件正反面时间

    investor_answers = db.Column(db.JSON)          # 合格投资者测评结果
    investor_answers_time = db.Column(db.DateTime) # 合格投资者测评时间

    real_name_verify = db.Column(db.Boolean, default=False) # 实名认证结果
    real_name_verify_time = db.Column(db.DateTime)          # 实名认证时间
    real_name_image_url_key = db.Column(db.String(128))     # 实名认证照片
    real_name_bank_card = db.Column(db.String(32))          # 实名认证银行卡号

    risk_level = db.Column(db.String(4))            # 风险承受能力
    risk_level_score = db.Column(db.Integer)        # 风险测评得分
    risk_level_answers = db.Column(db.JSON)         # 风险测评结果
    risk_level_verify_time = db.Column(db.DateTime) # 风险测评时间
    risk_level_expire_time = db.Column(db.DateTime) # 风险测评过期时间

    asset_image_url_key = db.Column(db.String(128))      # 资产规模照片
    experience_image_url_key = db.Column(db.String(128)) # 投资经历照片

    experience_verify_time = db.Column(db.DateTime) # 投资者证明资料时间

    info_table_url_key = db.Column(db.String(128))           # 投资者信息表文件
    info_table_verify = db.Column(db.Boolean, default=False) # 投资者信息表结果
    info_table_verify_time = db.Column(db.DateTime)          # 投资者信息表时间

    commitment_url_key = db.Column(db.String(128))           # 合格投资者承诺函文件
    commitment_verify = db.Column(db.Boolean, default=False) # 合格投资者承诺函结果
    commitment_verify_time = db.Column(db.DateTime)          # 合格投资者承诺函时间


class InvestorInformation(BaseModel, InvestorMixin):
    """投资者认证信息表"""
    __tablename__ = 'investor_information'

    investor_id = db.Column(db.String(32), primary_key=True)

    secret = db.Column(db.String(128)) # 海峰用户密钥

    @classmethod
    def get_investor_information(cls, investor_id, remove_fields_list=None):
        remove_fields_list = ['secret', *(remove_fields_list or [])]
        self = cls.filter_by_query(investor_id=investor_id).one_or_none()
        if self is None:
            self = cls.create(investor_id=investor_id)
            db.session.refresh(self)
        return self.to_dict(remove_fields_list=remove_fields_list)

    @classmethod
    def update_investor_information(cls, investor_id, **data):
        self = cls.filter_by_query(investor_id=investor_id).one_or_none()
        if self is None:
            raise LogicError('投资者认证信息不存在')

        self.update(**data)
        db.session.refresh(self)
        return self.to_dict()


class InvestorCertification(BaseModel, InvestorMixin):
    """合格投资者认证结果"""
    __tablename__ = 'investor_certification'

    id = db.Column(db.Integer, primary_key=True)
    investor_id = db.Column(db.String(32))
    manager_id = db.Column(db.String(32))

    certification_status = db.Column(db.String(20))         # 认证状态: CertificationStatus
    certification_error_message = db.Column(db.String(128)) # 认证失败信息
    is_professional = db.Column(db.Boolean, default=False)  # 是否专业投资者
    is_effective = db.Column(db.Boolean, default=False)     # 是否生效
    is_latest = db.Column(db.Boolean, default=True)         # 是否最新

    def get_investor_certification(self, refresh=False):
        if refresh:
            db.session.refresh(self)

        investor_certification = self.to_dict()
        if self.certification_status == CertificationStatus.VERIFYING:
            investor_certification.update(InvestorInformation.get_investor_information(
                self.investor_id, remove_fields_list=['create_time', 'update_time']
            ))
        return investor_certification

    @classmethod
    def get_latest_certification(cls, investor_id, manager_id):
        self = cls.filter_by_query(investor_id=investor_id, manager_id=manager_id, is_latest=True).one_or_none()
        if self is not None:
            return self.get_investor_certification()

    @classmethod
    def get_effective_certification(cls, investor_id, manager_id):
        self = cls.filter_by_query(investor_id=investor_id, manager_id=manager_id, is_effective=True).one_or_none()
        if self is not None:
            return self.get_investor_certification()

    @classmethod
    def check_latest_certification(cls, investor_id, manager_id):
        self = cls.filter_by_query(investor_id=investor_id, manager_id=manager_id, is_latest=True).one_or_none()
        if self is None:
            raise LogicError('认证信息不存在，请先申请认证！')
        return self

    @classmethod
    def apply_certification(cls, investor_id, manager_id):
        self = cls.filter_by_query(investor_id=investor_id, manager_id=manager_id, is_latest=True).one_or_none()
        if self is not None:
            raise LogicError('认证信息已存在！')

        self = cls.create(
            investor_id=investor_id,
            manager_id=manager_id,
            certification_status=CertificationStatus.VERIFYING,
        )
        return self.get_investor_certification(refresh=True)

    @classmethod
    def submit_certification(cls, investor_id, manager_id):
        self = cls.check_latest_certification(investor_id, manager_id)
        if self.certification_status != CertificationStatus.VERIFYING:
            raise LogicError('已提交审核！')

        investor_information = InvestorInformation.get_investor_information(
            investor_id, remove_fields_list=['create_time', 'update_time']
        )
        self.update(
            **investor_information,
            certification_status=CertificationStatus.REVIEWING,
        )
        return self.get_investor_certification(refresh=True)

    @classmethod
    def approve_certification(cls, investor_id, manager_id, is_professional=False):
        self = cls.check_latest_certification(investor_id, manager_id)
        if self.certification_status != CertificationStatus.REVIEWING:
            raise LogicError('无待审核信息，不能审核！')

        old = cls.filter_by_query(investor_id=investor_id, manager_id=manager_id, is_effective=True).one_or_none()
        if old:
            old.is_effective = False

        self.update(
            certification_status=CertificationStatus.REVIEW_SUCCESSFUL,
            is_professional=is_professional,
            is_effective=True,
        )
        return self.get_investor_certification(refresh=True)

    @classmethod
    def unapprove_certification(cls, investor_id, manager_id, error_message=None):
        self = cls.check_latest_certification(investor_id, manager_id)
        if self.certification_status != CertificationStatus.REVIEWING:
            raise LogicError('无待审核信息，不能审核！')

        self.update(
            certification_status=CertificationStatus.REVIEW_FAILED,
            certification_error_message=error_message,
        )
        return self.get_investor_certification(refresh=True)

    @classmethod
    def reapply_certification(cls, investor_id, manager_id):
        self = cls.check_latest_certification(investor_id, manager_id)
        if self.certification_status == CertificationStatus.VERIFYING:
            raise LogicError('认证中，无需重新认证！')

        if self.certification_status == CertificationStatus.REVIEWING:
            self.update(certification_status=CertificationStatus.VERIFYING)
        else:
            self.is_latest = False
            self = cls.create(
                investor_id=investor_id,
                manager_id=manager_id,
                certification_status=CertificationStatus.VERIFYING,
            )
        return self.get_investor_certification(refresh=True)


class InvestorContract(BaseModel):
    """投资者签约合同"""
    __tablename__ = 'investor_contract'

    id = db.Column(db.Integer, primary_key=True)
    investor_id = db.Column(db.String(32))
    manager_id = db.Column(db.String(32))
    fof_id = db.Column(db.String(16))

    contract_status = db.Column(db.String(8)) # 签约状态: ContractStatus
    order_id = db.Column(db.String(64))       # 签约编号

    book_amount = db.Column(db.Float)      # 预约金额
    book_name = db.Column(db.String(10))   # 预约姓名
    book_mobile = db.Column(db.String(20)) # 预约电话
    book_date = db.Column(db.DateTime)     # 预约时间

    risk_disclose_url_key = db.Column(db.String(128))           # 风险揭示书文件
    risk_disclose_verify = db.Column(db.Boolean, default=False) # 风险揭示书结果
    risk_disclose_verify_time = db.Column(db.DateTime)          # 风险揭示书时间

    fund_contract_url_key = db.Column(db.String(128))           # 基金合同签署文件
    fund_contract_verify = db.Column(db.Boolean, default=False) # 基金合同签署结果
    fund_contract_verify_time = db.Column(db.DateTime)          # 基金合同签署时间

    protocol_url_key = db.Column(db.String(128))           # 补充协议文件
    protocol_verify = db.Column(db.Boolean, default=False) # 补充协议结果
    protocol_verify_time = db.Column(db.DateTime)          # 补充协议时间

    fund_matching_url_key = db.Column(db.String(128))           # 风险匹配告知书文件
    fund_matching_verify = db.Column(db.Boolean, default=False) # 风险匹配告知书结果
    fund_matching_verify_time = db.Column(db.DateTime)          # 风险匹配告知书时间

    video_url_key = db.Column(db.String(128))           # 双录视频文件
    video_verify = db.Column(db.Boolean, default=False) # 双录视频结果
    video_verify_time = db.Column(db.DateTime)          # 双录视频时间

    lookback_url_key = db.Column(db.String(128))           # 回访确认书文件
    lookback_verify = db.Column(db.Boolean, default=False) # 回访确认书结果
    lookback_verify_time = db.Column(db.DateTime)          # 回访确认书时间

    def get_contract(self):
        db.session.refresh(self)
        return self.to_dict()

    @classmethod
    def get_investor_contract(cls, investor_id, manager_id, fof_id):
        self = cls.filter_by_query(investor_id=investor_id, manager_id=manager_id, fof_id=fof_id).one_or_none()
        if self is not None:
            return self.to_dict()

    @classmethod
    def get_investor_contracts(cls, investor_id, manager_id):
        instances = cls.filter_by_query(investor_id=investor_id, manager_id=manager_id).all()
        return [instance.to_dict() for instance in instances]

    @classmethod
    def get_manager_contracts(cls, manager_id):
        fields_list = {
            'id', 'investor_id', 'manager_id', 'fof_id',
            'book_amount', 'book_name', 'book_mobile', 'book_date',
            'contract_status', 'order_id', 'update_time',
        }
        instances = cls.filter_by_query(manager_id=manager_id).all()
        return [instance.to_dict(fields_list=fields_list) for instance in instances]

    @classmethod
    def check_contract(cls, investor_id, manager_id, fof_id):
        self = cls.filter_by_query(investor_id=investor_id, manager_id=manager_id, fof_id=fof_id).one_or_none()
        if self is None:
            raise LogicError('签约信息不存在，请先预约！')
        return self

    @classmethod
    def update_investor_contract(cls, investor_id, manager_id, fof_id, **data):
        self = cls.check_contract(investor_id=investor_id, manager_id=manager_id, fof_id=fof_id)
        if self.contract_status == ContractStatus.BOOKED:
            raise LogicError('预约未处理！')
        elif self.contract_status == ContractStatus.SIGNED:
            raise LogicError('签约已完成！')

        self.update(**data)
        if all((self.risk_disclose_verify, self.fund_contract_verify, self.protocol_verify,
                self.fund_matching_verify, self.video_verify, self.lookback_verify)):
            self.update(contract_status=ContractStatus.SIGNED)
        return self.get_contract()

    @classmethod
    def book_contract(cls, investor_id, manager_id, fof_id, **data):
        self = cls.filter_by_query(investor_id=investor_id, manager_id=manager_id, fof_id=fof_id).one_or_none()
        if self is not None:
            raise LogicError('签约信息已存在！')

        if InvestorCertification.get_effective_certification(investor_id, manager_id) is None:
            raise LogicError('未完成合格投资者认证，无法预约！')

        self = cls.create(
            investor_id=investor_id,
            manager_id=manager_id,
            fof_id=fof_id,
            contract_status=ContractStatus.BOOKED,
            order_id=uuid.uuid1().hex,
            **data,
        )
        return self.get_contract()

    @classmethod
    def signing_contract(cls, investor_id, manager_id, fof_id):
        self = cls.check_contract(investor_id, manager_id, fof_id)
        if self.contract_status != ContractStatus.BOOKED:
            raise LogicError('预约已处理！')

        self.update(contract_status=ContractStatus.SIGNING)
        return self.get_contract()

