
from pydantic import constr

from bases.validation import UnitValidation


class ApproveValidation(UnitValidation):
    """sync with InvestorCertification"""
    is_professional: bool = False # 是否是专业投资者


class UnapproveValidation(UnitValidation):
    """sync with InvestorCertification"""
    error_message: constr(max_length=128) = None # 认证失败信息

