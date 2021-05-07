
import requests

from flask import current_app

from bases.constants import HaiFengTemplateType, HaiFengCertType, TemplateStatus
from bases.exceptions import LogicError
from bases.globals import db, settings
from extensions.s3.pdf_store import PdfStore
from models import ProductionContract, ProductionSignStatus, ProductionTemplate

from .haifeng_token import HaiFengToken


class FOFTemplate:

    def __init__(self):
        self.host = settings['HAI_FENG']['host']

    def _parse_data(self, data):
        if data['success'] != 1:
            current_app.logger.error(f'[FOFTemplate] Failed! (data){data}')
            return
        return data['data']

    def _request(self, endpoint, params=None):
        headers = HaiFengToken().get_headers()
        response = requests.post(self.host + endpoint, json=params, timeout=5, headers=headers)

        data = response.json()
        current_app.logger.info(f'[FOFTemplate] (endpoint){endpoint} (data){data} (params){params}')
        return data

    ###########
    # Manager #
    ###########

    def get_products(self, manager_id) -> 'list | None':
        endpoint = '/v2/contract/getProductList'
        params = {'extId': manager_id}
        return self._parse_data(self._request(endpoint, params))

    def get_templates(self, manager_id, product_id: int) -> 'list | None':
        endpoint = '/v2/contract/getTemplateListByProduct'
        params = {'extId': manager_id, 'productId': product_id}
        return self._parse_data(self._request(endpoint, params))

    def get_template_detail(self, manager_id, template_id) -> 'dict | None':
        endpoint = '/v2/contract/getTemplateInfo'
        params = {'extId': manager_id, 'contractTemplateId': template_id}
        return self._parse_data(self._request(endpoint, params))

    def get_template_download_url(self, manager_id, template_id) -> 'str | None':
        template_detail = self.get_template_detail(manager_id, template_id)
        if not template_detail:
            return
        return template_detail['downloadUrl']

    def get_contract_detail(self, manager_id, contract_id) -> 'dict | None':
        endpoint = '/v2/contract/getContractInfo'
        params = {'extId': manager_id, 'contractId': contract_id}
        return self._parse_data(self._request(endpoint, params))

    def get_contract_download_url(self, manager_id, contract_id) -> str:
        contract_detail = self.get_contract_detail(manager_id, contract_id)
        if not contract_detail:
            raise LogicError('获取合同文件失败!')
        return contract_detail['contractFileUrl']

    ############
    # Investor #
    ############

    def register_investor(self, investor_id, investor_info: dict):
        endpoint = '/v2/InfoProvision/setIndividualInfo'
        params = {
            'individualId': investor_id,
            'individualName': investor_info['name'],
            'individualCertType': HaiFengCertType.parse(investor_info['cert_type']),
            'individualCertNum': investor_info['cert_num'],
            'individualPhoneNum': investor_info['mobile_phone'],
            'individualEmail': investor_info['email'],
        }
        data = self._request(endpoint, params)

        if data['success'] != 1:
            current_app.logger.error(f'[register_investor] Failed! (data){data}')
            return data['message']

    def generate_contract(self, manager_id, template_id, investor_id) -> 'int | None':
        endpoint = '/v2/InfoProvision/setContractInfo'
        params = {
            'extId': manager_id,
            'individualId': investor_id,
            'investorType': 1, # 1: 个人; 2: 机构
            'contractTemplateId': template_id,
        }
        data = self._request(endpoint, params)

        if data['success'] != 1:
            current_app.logger.error(f'[generate_contract] Failed! (data){data}')
            return
        return data['data']['contractId']

    ############
    # Function #
    ############

    def save_fof_template(self, manager_id, fof_id):
        # TODO: use products[fof_id]
        # products = self.get_products(manager_id)
        # products = {product['productCode']: product['productId'] for product in products}
        # if fof_id not in products:
        #     current_app.logger.info(f'[FOFTemplate] product not found (fof_id){fof_id}')
        #     return False

        # templates = self.get_templates(manager_id, products[fof_id])
        templates = self.get_templates(manager_id, 2064)
        if not templates:
            current_app.logger.info(f'[FOFTemplate] product no templates (fof_id){fof_id}')
            return False

        template_ids = ProductionTemplate.filter_by_query().all()
        template_ids = set(template_id.template_id for template_id in template_ids)

        flag = False
        for template in templates:
            template_type = HaiFengTemplateType.read(template['contractTemplateType'])
            if not template_type:
                continue
            template_id = template['contractTemplateId']
            if template_id in template_ids:
                continue

            template_url = self.get_template_download_url(manager_id, template_id)
            if not template_url:
                continue
            template_url_key = PdfStore().store_template_pdf(template_url, template_id)

            ProductionTemplate(
                template_id=template_id,
                fof_id=fof_id,
                manager_id=manager_id,
                template_type=template_type,
                template_name=template['contractTemplateName'],
                template_url_key=template_url_key,
                signed=(template['contractTemplateStatus'] == 2),
            ).save(commit=False)
            flag = True

        if flag:
            db.session.commit()
        return flag

    def generate_contracts(self, investor_id, manager_id, fof_id):
        production_template = ProductionSignStatus.filter_by_query(fof_id=fof_id, manager_id=manager_id).first()
        if not production_template:
            raise LogicError('产品合同模板未上架！')
        if production_template.template_status != TemplateStatus.COMPLETED:
            raise LogicError('产品合同模板未签署完成！')

        templates = ProductionTemplate.get_template_ids(fof_id)
        for template_type, template_id in templates.items():
            contract_id = self.generate_contract(manager_id, template_id, investor_id)
            if not contract_id:
                raise LogicError('生成投资者产品合同失败！')
            contract_detail = self.get_contract_detail(manager_id, contract_id)
            if not contract_detail:
                raise LogicError('获取产品合同详情失败！')
            contract_url_key = PdfStore().store_contract_pdf(investor_id, contract_detail['contractFileUrl'], contract_id)

            ProductionContract(
                investor_id=investor_id,
                manager_id=manager_id,
                fof_id=fof_id,
                template_id=template_id,
                template_type=template_type,
                contract_id=contract_id,
                contract_url_key=contract_url_key,
                union_key=contract_detail['unionKey'],
            ).save(commit=False)

        db.session.commit()

