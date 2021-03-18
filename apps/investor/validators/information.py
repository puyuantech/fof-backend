import datetime

from pydantic import Field, conint, constr
from typing import Optional, List

from bases.constants import RISK_LEVEL_EXPIRE_DAY
from bases.validation import InvestorValidation


class FaceImageValidation(InvestorValidation):
    """sync with InvestorInformation"""
    face_image_url_key: constr(max_length=128) # 人脸识别照片
    face_image_verify_time: datetime.datetime = Field(default_factory=datetime.datetime.now)


class CertImageValidation(InvestorValidation):
    """sync with InvestorInformation"""
    cert_front_image_url_key: constr(max_length=128) # 证件正面照片
    cert_back_image_url_key: constr(max_length=128)  # 证件反面照片
    cert_image_time: datetime.datetime = Field(default_factory=datetime.datetime.now)


class RealNameValidation(InvestorValidation):
    """sync with InvestorInformation"""
    name: constr(max_length=10)                     # 姓名
    email: Optional[constr(max_length=64)]          # 邮箱
    nationality: constr(max_length=32)              # 国籍
    gender: conint(ge=1, le=2)                      # 性别(1: 男, 2: 女)
    age: int                                        # 年龄
    mobile_phone: constr(max_length=20)             # 手机
    landline_phone: Optional[constr(max_length=20)] # 座机
    profession: constr(max_length=32)               # 职业
    job: constr(max_length=32)                      # 职务
    postcode: Optional[constr(max_length=20)]       # 邮编
    address: Optional[constr(max_length=256)]       # 住址

    cert_type: constr(max_length=10)                # 证件类型
    cert_num: constr(max_length=32)                 # 证件编号
    cert_expire_date: datetime.date                 # 证件过期时间(input: '%Y-%m-%d')

    investor_answers: List[str]                     # 合格投资者测评结果

    secret: constr(max_length=128) = None           # 海峰用户密钥
    real_name_verify: bool                          # 实名认证结果
    real_name_verify_time: datetime.datetime = Field(default_factory=datetime.datetime.now)


class RiskLevelValidation(InvestorValidation):
    """sync with InvestorInformation"""
    risk_level_answers: List[str] # 风险测评结果
    risk_level_verify_time: datetime.datetime = Field(default_factory=datetime.datetime.now)
    risk_level_expire_time: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now() + datetime.timedelta(days=RISK_LEVEL_EXPIRE_DAY)
    )


class ExperienceValidation(InvestorValidation):
    """sync with InvestorInformation"""
    asset_image_url_key: constr(max_length=128)      # 资产规模照片
    experience_image_url_key: constr(max_length=128) # 投资经历照片
    experience_verify_time: datetime.datetime = Field(default_factory=datetime.datetime.now)


class InfoTableValidation(InvestorValidation):
    """sync with InvestorInformation"""
    info_table: constr(max_length=128)                # 投资者信息表链接
    info_table_url_key: constr(max_length=128) = None # 投资者信息表文件
    info_table_verify: bool                           # 投资者信息表结果
    info_table_verify_time: datetime.datetime = Field(default_factory=datetime.datetime.now)


class CommitmentValidation(InvestorValidation):
    """sync with InvestorInformation"""
    commitment: constr(max_length=128)                # 合格投资者承诺函链接
    commitment_url_key: constr(max_length=128) = None # 合格投资者承诺函文件
    commitment_verify: bool                           # 合格投资者承诺函结果
    commitment_verify_time: datetime.datetime = Field(default_factory=datetime.datetime.now)

