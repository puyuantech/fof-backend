
from bases.validation import FOFValidation, UnitValidation, ContractValidation
from bases.viewhandler import ApiViewHandler
from models import InvestorContract, ContractTemplate
from utils.decorators import login_required

from .libs import fill_investor_contract, fill_investor_contracts, get_contract_url_key
from .validators.contract import (RiskDiscloseValidation, FundContractValidation, ProtocolValidation,
                                  FundMatchingValidation, VideoValidation, LookbackValidation, BookValidation)


class ContractAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = ContractValidation.get_valid_data(self.input)
        investor_contract = InvestorContract.get_investor_contract(**data)
        return fill_investor_contract(investor_contract)


class ContractListAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = UnitValidation.get_valid_data(self.input)
        investor_contracts = InvestorContract.get_investor_contracts(**data)
        return fill_investor_contracts(investor_contracts)


class ContractTemplateAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = FOFValidation.get_valid_data(self.input)
        return ContractTemplate.get_template_ids(**data)


class RiskDiscloseAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = RiskDiscloseValidation.get_valid_data(self.input)
        data['risk_disclose_url_key'] = get_contract_url_key(data.pop('risk_disclose'), data['manager_id'])
        investor_contract = InvestorContract.update_investor_contract(**data)
        return fill_investor_contract(investor_contract)


class FundContractAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FundContractValidation.get_valid_data(self.input)
        data['fund_contract_url_key'] = get_contract_url_key(data.pop('fund_contract'), data['manager_id'])
        investor_contract = InvestorContract.update_investor_contract(**data)
        return fill_investor_contract(investor_contract)


class ProtocolAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ProtocolValidation.get_valid_data(self.input)
        data['protocol_url_key'] = get_contract_url_key(data.pop('protocol'), data['manager_id'])
        investor_contract = InvestorContract.update_investor_contract(**data)
        return fill_investor_contract(investor_contract)


class FundMatchingAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FundMatchingValidation.get_valid_data(self.input)
        data['fund_matching_url_key'] = get_contract_url_key(data.pop('fund_matching'), data['manager_id'])
        investor_contract = InvestorContract.update_investor_contract(**data)
        return fill_investor_contract(investor_contract)


class VideoAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = VideoValidation.get_valid_data(self.input)
        data['video_url_key'] = get_contract_url_key(data.pop('video'), data['manager_id'])
        investor_contract = InvestorContract.update_investor_contract(**data)
        return fill_investor_contract(investor_contract)


class LookbackAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = LookbackValidation.get_valid_data(self.input)
        data['lookback_url_key'] = get_contract_url_key(data.pop('lookback'), data['manager_id'])
        investor_contract = InvestorContract.update_investor_contract(**data)
        return fill_investor_contract(investor_contract)


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

