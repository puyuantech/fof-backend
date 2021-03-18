
from flask import g

from extensions.haifeng.fof_template import FOFTemplate
from extensions.s3.pdf_store import PdfStore


def get_contract_url_key(contract_id, manager_id):
    contract_url = FOFTemplate().get_contract_download_url(contract_id, manager_id)
    return PdfStore().store_contract_pdf(g.user.id, contract_url, contract_id)

