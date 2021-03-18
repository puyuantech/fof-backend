
from bases.constants import ContractStatus
from bases.validation import FOFValidation, UnitValidation, ContractValidation
from bases.viewhandler import ApiViewHandler
from models import InvestorCertification, InvestorContract, FOFInfo, ContractTemplate
from utils.decorators import login_required

from .libs import get_contract_url_key
from .validators.contract import (RiskDiscloseValidation, FundContractValidation, ProtocolValidation,
                                  FundMatchingValidation, VideoValidation, LookbackValidation, BookValidation)


class ContractAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = ContractValidation.get_valid_data(self.input)
        investor_contract = InvestorContract.get_investor_contract(**data)
        if investor_contract:
            cert_num = InvestorCertification.get_effective_certification(
                data['investor_id'], data['manager_id']
            )['cert_num']
            fof_info = FOFInfo.get_by_query(fof_id=investor_contract['fof_id'])

            investor_contract.update({
                'cert_num': cert_num[:4] + '************' + cert_num[-2:],
                'fof_name': fof_info.fof_name,
            })
        return investor_contract


class ContractListAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = UnitValidation.get_valid_data(self.input)
        investor_contracts = InvestorContract.get_investor_contracts(**data)

        fofs = FOFInfo.filter_by_query(manager_id=data['manager_id']).all()
        fofs = {
            fof.fof_id: {
                'fof_name': fof.fof_name,
                'risk_type': fof.risk_type,
            } for fof in fofs
        }

        for investor_contract in investor_contracts:
            investor_contract.update(fofs.pop(investor_contract['fof_id']))

        for fof_id, fof_info in fofs.items():
            investor_contracts.append({
                'contract_status': ContractStatus.UNBOOKED,
                'fof_id': fof_id,
                **fof_info,
            })

        return investor_contracts


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
        return InvestorContract.update_investor_contract(**data)


class FundContractAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FundContractValidation.get_valid_data(self.input)
        data['fund_contract_url_key'] = get_contract_url_key(data.pop('fund_contract'), data['manager_id'])
        return InvestorContract.update_investor_contract(**data)


class ProtocolAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ProtocolValidation.get_valid_data(self.input)
        data['protocol_url_key'] = get_contract_url_key(data.pop('protocol'), data['manager_id'])
        return InvestorContract.update_investor_contract(**data)


class FundMatchingAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FundMatchingValidation.get_valid_data(self.input)
        data['fund_matching_url_key'] = get_contract_url_key(data.pop('fund_matching'), data['manager_id'])
        return InvestorContract.update_investor_contract(**data)


class VideoAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = VideoValidation.get_valid_data(self.input)
        data['video_url_key'] = get_contract_url_key(data.pop('video'), data['manager_id'])
        return InvestorContract.update_investor_contract(**data)


class LookbackAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = LookbackValidation.get_valid_data(self.input)
        data['lookback_url_key'] = get_contract_url_key(data.pop('lookback'), data['manager_id'])
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

