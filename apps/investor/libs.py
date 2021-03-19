
from flask import g

from extensions.haifeng.fof_template import FOFTemplate
from extensions.s3.pdf_store import PdfStore
from models import InvestorCertification, FOFInfo


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


def get_contract_url_key(contract_id, manager_id):
    contract_url = FOFTemplate().get_contract_download_url(contract_id, manager_id)
    return PdfStore().store_contract_pdf(g.user.id, contract_url, contract_id)

