
from bases.validation import UnitValidation, ContractValidation
from bases.viewhandler import ApiViewHandler
from models import InvestorContract
from utils.decorators import login_required

from .validators.contract import (RiskDiscloseValidation, FundContractValidation, ProtocolValidation,
                                  FundMatchingValidation, VideoValidation, LookbackValidation, BookValidation)


class ContractAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = ContractValidation.get_valid_data(self.input)
        return InvestorContract.get_investor_contract(**data)


class ContractListAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = UnitValidation.get_valid_data(self.input)
        return InvestorContract.get_investor_contracts(**data)


class RiskDiscloseAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = RiskDiscloseValidation.get_valid_data(self.input)
        data['risk_disclose_url_key'] = data.pop('risk_disclose')
        return InvestorContract.update_investor_contract(**data)


class FundContractAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FundContractValidation.get_valid_data(self.input)
        data['fund_contract_url_key'] = data.pop('fund_contract')
        return InvestorContract.update_investor_contract(**data)


class ProtocolAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ProtocolValidation.get_valid_data(self.input)
        data['protocol_url_key'] = data.pop('protocol')
        return InvestorContract.update_investor_contract(**data)


class FundMatchingAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FundMatchingValidation.get_valid_data(self.input)
        data['fund_matching_url_key'] = data.pop('fund_matching')
        return InvestorContract.update_investor_contract(**data)


class VideoAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = VideoValidation.get_valid_data(self.input)
        data['video_url_key'] = data.pop('video')
        return InvestorContract.update_investor_contract(**data)


class LookbackAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = LookbackValidation.get_valid_data(self.input)
        data['lookback_url_key'] = data.pop('lookback')
        return InvestorContract.update_investor_contract(**data)


class BookAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = BookValidation.get_valid_data(self.input)
        return InvestorContract.book_contract(**data)


class SignAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ContractValidation.get_valid_data(self.input)
        return InvestorContract.signing_contract(**data)

