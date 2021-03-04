import datetime

from pydantic import Field, constr

from bases.validation import ContractValidation


class RiskDiscloseValidation(ContractValidation):
    """sync with InvestorContract"""
    risk_disclose: constr(max_length=128)                # 风险揭示书链接
    risk_disclose_url_key: constr(max_length=128) = None # 风险揭示书文件
    risk_disclose_verify: bool                           # 风险揭示书结果
    risk_disclose_verify_time: datetime.datetime = Field(default_factory=datetime.datetime.now)


class FundContractValidation(ContractValidation):
    """sync with InvestorContract"""
    fund_contract: constr(max_length=128)                # 基金合同签署链接
    fund_contract_url_key: constr(max_length=128) = None # 基金合同签署文件
    fund_contract_verify: bool                           # 基金合同签署结果
    fund_contract_verify_time: datetime.datetime = Field(default_factory=datetime.datetime.now)


class ProtocolValidation(ContractValidation):
    """sync with InvestorContract"""
    protocol: constr(max_length=128)                # 补充协议链接
    protocol_url_key: constr(max_length=128) = None # 补充协议文件
    protocol_verify: bool                           # 补充协议结果
    protocol_verify_time: datetime.datetime = Field(default_factory=datetime.datetime.now)


class FundMatchingValidation(ContractValidation):
    """sync with InvestorContract"""
    fund_matching: constr(max_length=128)                # 风险匹配告知书链接
    fund_matching_url_key: constr(max_length=128) = None # 风险匹配告知书文件
    fund_matching_verify: bool                           # 风险匹配告知书结果
    fund_matching_verify_time: datetime.datetime = Field(default_factory=datetime.datetime.now)


class VideoValidation(ContractValidation):
    """sync with InvestorContract"""
    video: constr(max_length=128)                # 双录视频链接
    video_url_key: constr(max_length=128) = None # 双录视频文件
    video_verify: bool                           # 双录视频结果
    video_verify_time: datetime.datetime = Field(default_factory=datetime.datetime.now)


class LookbackValidation(ContractValidation):
    """sync with InvestorContract"""
    lookback: constr(max_length=128)                # 回访确认书链接
    lookback_url_key: constr(max_length=128) = None # 回访确认书文件
    lookback_verify: bool                           # 回访确认书结果
    lookback_verify_time: datetime.datetime = Field(default_factory=datetime.datetime.now)


class BookValidation(ContractValidation):
    """sync with InvestorContract"""
    book_amount: float                 # 预约金额
    book_name: constr(max_length=10)   # 预约姓名
    book_mobile: constr(max_length=20) # 预约电话
    book_date: datetime.datetime = Field(default_factory=datetime.datetime.now)

