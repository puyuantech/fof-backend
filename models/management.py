
from bases.dbwrapper import db, BaseModel


class Management(BaseModel):
    """私募基金管理人"""
    __tablename__ = 'managements'

    # from list
    manager_id = db.Column(db.String(16), primary_key=True)
    manager_name = db.Column(db.String(128))     # 私募基金管理人名称
    person_name = db.Column(db.String(32))       # 法定代表人/执行事务合伙人(委派代表)姓名
    invest_type = db.Column(db.String(32))       # 机构类型
    register_no = db.Column(db.String(8))        # 登记编号
    member_type = db.Column(db.String(8))        # 会员类型
    has_special_tips = db.Column(db.Boolean)     # 是否有提示信息
    has_credit_tips = db.Column(db.Boolean)      # 是否有诚信信息
    establish_date = db.Column(db.Date)          # 成立时间
    register_date = db.Column(db.Date)           # 登记时间
    fund_count = db.Column(db.Integer)           # 在管基金数量

    office_province = db.Column(db.String(16))   # 办公地
    office_city = db.Column(db.String(16))       # 办公城市
    office_address = db.Column(db.String(128))   # 办公地址

    register_province = db.Column(db.String(16)) # 注册地
    register_city = db.Column(db.String(16))     # 注册城市
    register_address = db.Column(db.String(128)) # 注册地址

    # 机构信息
    manager_name_en = db.Column(db.String(128))  # 基金管理人全称(英文)
    organization_code = db.Column(db.String(32)) # 组织机构代码
    register_capital = db.Column(db.Float)       # 注册资本(万元): 10,526.32
    register_currency = db.Column(db.String(8))  # 注册资本币种: 人民币、美元、港元
    payment_capital = db.Column(db.Float)        # 实缴资本(万元)
    payment_currency = db.Column(db.String(8))   # 实缴资本币种: 人民币、美元、港元
    payment_ratio = db.Column(db.Float)          # 注册资本实缴比例: 55.006%
    enterprise_nature = db.Column(db.String(16)) # 企业性质
    business_type = db.Column(db.JSON)           # 业务类型
    employee_count = db.Column(db.Integer)       # 全职员工人数
    practitioner_count = db.Column(db.Integer)   # 取得基金从业人数
    website = db.Column(db.String(128))          # 机构网址
    manager_size = db.Column(db.String(16))      # 管理规模区间

    # 会员信息
    is_member = db.Column(db.String(1))              # 是否为会员
    member_representative = db.Column(db.String(32)) # 会员代表
    current_member_type = db.Column(db.String(8))    # 当前会员类型
    member_time = db.Column(db.Date)                 # 入会时间

    # 法律意见书信息
    legal_opinion_status = db.Column(db.String(8)) # 法律意见书状态
    law_firm_name = db.Column(db.String(32))       # 律师事务所名称
    lawyer_name = db.Column(db.String(32))         # 律师事务所名称

    # 实际控制人信息
    controller_name = db.Column(db.String(128))  # 实际控制人姓名 / 名称

    # 高管信息
    # 关联方信息（仅包含关联私募基金管理人）
    # 出资人信息

    update_date = db.Column(db.Date)             # 机构信息最后更新时间
    fund_ids = db.Column(db.JSON)                # 产品信息

    def to_list_dict(self):
        return {
            'manager_id': self.manager_id,
            'manager_name': self.manager_name,
            'register_no': self.register_no,
            'register_date': self.register_date.strftime('%Y-%m-%d'),
            'establish_date': self.establish_date.strftime('%Y-%m-%d'),
            'fund_count': self.fund_count,
            'manager_size': self.manager_size,
            'invest_type': self.invest_type,
            'business_type': self.business_type,
            'website': self.website,
        }


class ManagementFund(BaseModel):
    """私募基金"""
    __tablename__ = 'management_funds'

    fund_id = db.Column(db.String(16), primary_key=True)

    fund_name = db.Column(db.String(128))      # 基金名称
    fund_no = db.Column(db.String(6))          # 基金编号
    establish_date = db.Column(db.Date)        # 成立时间
    filing_date = db.Column(db.Date)           # 备案时间
    filing_stage = db.Column(db.String(16))    # 基金备案阶段
    fund_type = db.Column(db.String(16))       # 基金类型
    currency_type = db.Column(db.String(16))   # 币种
    management_type = db.Column(db.String(16)) # 管理类型
    custodian_name = db.Column(db.String(128)) # 托管人名称
    fund_status = db.Column(db.String(16))     # 运作状态
    special_reminder = db.Column(db.Text)      # 基金业协会特别提示（针对基金）
    update_date = db.Column(db.Date)           # 基金信息最后更新时间
    manager_ids = db.Column(db.JSON)

