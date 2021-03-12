import datetime

from typing import List
from pydantic import BaseModel, constr


class ManagementBaseValidation(BaseModel):
    """sync with Manager"""
    manager_id: constr(max_length=16)
    manager_name: constr(max_length=128)
    person_name: constr(max_length=32)
    invest_type: constr(max_length=32)
    register_no: constr(max_length=8)
    member_type: constr(max_length=8)
    has_special_tips: bool
    has_credit_tips: bool
    establish_date: datetime.date
    register_date: datetime.date
    fund_count: int
    office_province: constr(max_length=16)
    office_city: constr(max_length=16)
    office_address: constr(max_length=128) = None
    register_province: constr(max_length=16)
    register_city: constr(max_length=16)
    register_address: constr(max_length=128) = None

    @classmethod
    def get_manager(cls, data: dict):
        return cls(
            manager_id=data['id'],
            manager_name=data['managerName'],
            person_name=data['artificialPersonName'],
            invest_type=data['primaryInvestType'],
            register_no=data['registerNo'],
            member_type=data['memberType'],
            has_special_tips=data['hasSpecialTips'],
            has_credit_tips=data['hasCreditTips'],
            establish_date=data['establishDate'],
            register_date=data['registerDate'],
            fund_count=data['fundCount'],
            office_province=data['officeProvince'],
            office_city=data['officeCity'],
            office_address=data['officeAddress'],
            register_province=data['registerProvince'],
            register_city=data['registerCity'],
            register_address=data['registerAddress'],
        )


class ManagementInfoValidation(BaseModel):
    """sync with Manager"""
    manager_name_en: constr(max_length=128) = None
    organization_code: constr(max_length=32)
    register_capital: float
    register_currency: constr(max_length=8)
    payment_capital: float
    payment_currency: constr(max_length=8)
    payment_ratio: float
    enterprise_nature: constr(max_length=16)
    business_type: List[str]
    employee_count: int = None
    practitioner_count: int = None
    website: constr(max_length=128) = None
    manager_size: constr(max_length=16)

    # 会员信息
    is_member: constr(max_length=1)
    member_representative: constr(max_length=32) = None
    current_member_type: constr(max_length=8) = None
    member_time: datetime.date = None

    # 法律意见书信息
    legal_opinion_status: constr(max_length=8)
    law_firm_name: constr(max_length=32) = None
    lawyer_name: constr(max_length=32) = None

    # 实际控制人信息
    controller_name: constr(max_length=128)

    update_date: datetime.date
    fund_ids: List[str]

    @staticmethod
    def get_capital_and_currency(data: dict, key: str):
        for currency in ('人民币', '美元', '港元'):
            capital = f'{key}(万元)({currency})'
            if capital not in data:
                continue
            return data[capital].replace(',', ''), currency
        return None, None

    @classmethod
    def get_manager(cls, data: dict):
        register_capital, register_currency = cls.get_capital_and_currency(data, '注册资本')
        payment_capital, payment_currency = cls.get_capital_and_currency(data, '实缴资本')
        return cls(
            manager_name_en=data['基金管理人全称(英文)'],
            organization_code=data['组织机构代码'],
            register_capital=register_capital,
            register_currency=register_currency,
            payment_capital=payment_capital,
            payment_currency=payment_currency,
            payment_ratio=data['注册资本实缴比例'].replace('%', '').replace(',', ''),
            enterprise_nature=data['企业性质'],
            business_type=[business.strip() for business in data['业务类型'].split('\n') if business.strip()],
            employee_count=data['全职员工人数:'],
            practitioner_count=data['取得基金从业人数'],
            website=(data['机构网址'] or None),
            manager_size=data['管理规模区间'],
            is_member=data['是否为会员'],
            member_representative=data.get('会员代表'),
            current_member_type=data.get('当前会员类型'),
            member_time=data.get('入会时间'),
            legal_opinion_status=data['法律意见书状态'],
            law_firm_name=data.get('律师事务所名称'),
            lawyer_name=data.get('律师姓名'),
            controller_name=data['实际控制人姓名 / 名称'],
            update_date=data['机构信息最后更新时间'],
            fund_ids=data['fund_ids'],
        )


class ManageFundValidation(BaseModel):
    """sync with ManagementFund"""
    fund_name: constr(max_length=128)
    fund_no: constr(max_length=32)
    establish_date: datetime.date
    filing_date: datetime.date
    filing_stage: constr(max_length=16) = None
    fund_type: constr(max_length=16)
    currency_type:  constr(max_length=16)
    management_type: constr(max_length=16)
    custodian_name: constr(max_length=128) = None
    fund_status: constr(max_length=16) = None
    special_reminder: str = None
    update_date: datetime.date
    manager_ids: List[str]

    @classmethod
    def get_fund(cls, data: dict):
        return cls(
            fund_name=data['基金名称:'],
            fund_no=data['基金编号:'],
            establish_date=data['成立时间:'],
            filing_date=data['备案时间:'],
            filing_stage=data.get('基金备案阶段:'),
            fund_type=data['基金类型:'],
            currency_type=data['币种:'],
            management_type=data['管理类型:'],
            custodian_name=data['托管人名称:'],
            fund_status=data['运作状态:'],
            special_reminder=data['基金业协会特别提示（针对基金）:'],
            update_date=data['基金信息最后更新时间:'],
            manager_ids=data['manager_ids'],
        )

