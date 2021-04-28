
from flask import g
from bases.validation import FOFValidation, ContractValidation
from bases.viewhandler import ApiViewHandler
from models import InvestorContract, ProductionContract
from utils.decorators import login_required

from .libs import fill_investor_contract, fill_investor_contracts, get_contract_url_key
from .validators.contract import (RiskDiscloseValidation, FundContractValidation, ProtocolValidation,
                                  FundMatchingValidation, VideoValidation, LookbackValidation, BookValidation)


class ContractAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = ContractValidation.get_valid_data(self.input)
        investor_contract = InvestorContract.get_investor_contract(manager_id=g.token.manager_id, **data)
        return fill_investor_contract(investor_contract)


class ContractListAPI(ApiViewHandler):

    @login_required
    def get(self):
        investor_contracts = InvestorContract.get_investor_contracts(g.token.investor_id, g.token.manager_id)
        return fill_investor_contracts(g.token.manager_id, investor_contracts)


class ContractTemplateAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = FOFValidation.get_valid_data(self.input)
        contracts = ProductionContract.filter_by_query(
            investor_id=g.token.investor_id,
            manager_id=g.token.manager_id,
            **data
        ).all()
        return {contract.template_type: contract.to_dict() for contract in contracts}


class RiskDiscloseAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = RiskDiscloseValidation.get_valid_data(self.input)
        data['risk_disclose_url_key'] = get_contract_url_key(data.pop('risk_disclose'))
        investor_contract = InvestorContract.update_investor_contract(
            g.token.investor_id, g.token.manager_id, **data)
        return fill_investor_contract(investor_contract)


class FundContractAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FundContractValidation.get_valid_data(self.input)
        data['fund_contract_url_key'] = get_contract_url_key(data.pop('fund_contract'))
        investor_contract = InvestorContract.update_investor_contract(
            g.token.investor_id, g.token.manager_id, **data)
        return fill_investor_contract(investor_contract)


class ProtocolAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ProtocolValidation.get_valid_data(self.input)
        data['protocol_url_key'] = get_contract_url_key(data.pop('protocol'))
        investor_contract = InvestorContract.update_investor_contract(
            g.token.investor_id, g.token.manager_id, **data)
        return fill_investor_contract(investor_contract)


class FundMatchingAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FundMatchingValidation.get_valid_data(self.input)
        data['fund_matching_url_key'] = get_contract_url_key(data.pop('fund_matching'))
        investor_contract = InvestorContract.update_investor_contract(
            g.token.investor_id, g.token.manager_id, **data)
        return fill_investor_contract(investor_contract)


class VideoAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = VideoValidation.get_valid_data(self.input)
        data['video_url_key'] = get_contract_url_key(data.pop('video'))
        investor_contract = InvestorContract.update_investor_contract(
            g.token.investor_id, g.token.manager_id, **data)
        return fill_investor_contract(investor_contract)


class LookbackAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = LookbackValidation.get_valid_data(self.input)
        data['lookback_url_key'] = get_contract_url_key(data.pop('lookback'))
        investor_contract = InvestorContract.update_investor_contract(
            g.token.investor_id, g.token.manager_id, **data)
        return fill_investor_contract(investor_contract)


class BookAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = BookValidation.get_valid_data(self.input)
        return InvestorContract.book_contract(
            g.token.investor_id, g.token.manager_id, **data)


class SignAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ContractValidation.get_valid_data(self.input)
        g.user_operation = '预约通过'
        g.user_operation_params = {
            'investor_id': data.get('investor_id'),
        }
        return InvestorContract.signing_contract(manager_id=g.token.manager_id, **data)

