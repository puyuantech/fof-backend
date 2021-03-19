
from flask import g
from typing import List

from bases.constants import ContractStatus
from extensions.haifeng.fof_template import FOFTemplate
from extensions.s3.pdf_store import PdfStore
from models import FOFInfo, InvestorCertification


def fill_investor_contract(investor_contract: dict):
    if investor_contract is None:
        return

    cert_num = InvestorCertification.get_effective_certification(
        investor_contract['investor_id'], investor_contract['manager_id']
    )['cert_num']
    fof_info = FOFInfo.get_by_query(fof_id=investor_contract['fof_id'])

    investor_contract.update({
        'cert_num': cert_num[:4] + '************' + cert_num[-2:],
        'fof_name': fof_info.fof_name,
    })
    return investor_contract


def fill_investor_contracts(manager_id, investor_contracts: List[dict]):
    fofs = FOFInfo.filter_by_query(manager_id=manager_id).all()
    fofs = {
        fof.fof_id: {'fof_name': fof.fof_name, 'risk_type': fof.risk_type}
        for fof in fofs
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


def get_contract_url_key(contract_id, manager_id):
    contract_url = FOFTemplate().get_contract_download_url(contract_id, manager_id)
    return PdfStore().store_contract_pdf(g.user.id, contract_url, contract_id)

