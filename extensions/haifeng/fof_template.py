
import requests

from flask import current_app

from bases.constants import HaiFengTemplateType
from bases.exceptions import LogicError
from bases.globals import db, settings
from extensions.s3.pdf_store import PdfStore
from models import ContractTemplate

from .manager_token import ManagerToken


class FOFTemplate:

    def __init__(self, manager_id):
        self.host = settings['HAI_FENG_HOST']
        self.manager_id = manager_id

    def _request(self, endpoint, params=None):
        headers = ManagerToken().get_headers(self.manager_id)
        response = requests.post(self.host + endpoint, json=params, timeout=5, headers=headers)
        data = response.json()
        if data['success'] != 1:
            current_app.logger.error(f'[FOFTemplate] Failed! (endpoint){endpoint} (data){data}')
            return
        return data['data']

    def get_products(self) -> 'list | None':
        endpoint = '/v2/contract/getProductList'
        return self._request(endpoint)

    def get_templates(self, product_id: int) -> 'list | None':
        endpoint = '/v2/contract/getTemplateListByProduct'
        params = {'productId': product_id}
        return self._request(endpoint, params)

    def get_template_detail(self, template_id) -> 'dict | None':
        endpoint = '/v2/contract/getTemplateInfo'
        params = {'contractTemplateId': template_id}
        return self._request(endpoint, params)

    def get_contract_detail(self, contract_id) -> 'dict | None':
        endpoint = '/v2/contract/getContractInfo'
        params = {'contractId': contract_id}
        return self._request(endpoint, params)

    def save_fof_template(self, fof_id):
        products = self.get_products()
        products = {product['productCode']: product['productId'] for product in products}
        if fof_id not in products:
            current_app.logger.info(f'[FOFTemplate] product not found (fof_id){fof_id}')
            return False

        templates = self.get_templates(products[fof_id])
        if not templates:
            return False

        template_ids = db.session.query(ContractTemplate.template_id).all()
        template_ids = set(template_id for template_id, in template_ids)

        for template in templates:
            template_type = HaiFengTemplateType.read(template['contractTemplateType'])
            if not template_type:
                continue
            template_id = template['contractTemplateId']
            if template_id in template_ids:
                continue

            template_url = self.get_template_download_url(template_id)
            template_url_key = PdfStore().store_template_pdf(template_url, template_id)

            ContractTemplate(
                template_id=template_id,
                fof_id=fof_id,
                manager_id=self.manager_id,
                template_type=template_type,
                template_url_key=template_url_key,
            ).save(commit=False)

        db.session.commit()
        return True

    def get_template_download_url(self, template_id) -> 'str | None':
        template_detail = self.get_template_detail(template_id)
        if not template_detail:
            return
        return template_detail['downloadUrl']

    def get_contract_download_url(self, contract_id) -> str:
        contract_detail = self.get_contract_detail(contract_id)
        if not contract_detail:
            raise LogicError('获取合同文件失败!')
        return contract_detail['contractFileUrl']

