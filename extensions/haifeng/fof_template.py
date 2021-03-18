
import requests

from flask import current_app

from bases.constants import HaiFengTemplateType
from bases.exceptions import LogicError
from bases.globals import db, settings
from models import ContractTemplate
from utils.helper import Singleton

from .manager_token import ManagerToken


class FOFTemplate(metaclass=Singleton):

    def __init__(self):
        self.host = settings['HAI_FENG_HOST']
        self.tokens = {}

    def _request(self, endpoint, params, manager_id):
        headers = ManagerToken().get_headers(manager_id)
        response = requests.post(self.host + endpoint, json=params, timeout=5, headers=headers)
        data = response.json()
        if data['success'] != 1:
            current_app.logger.error(f'[FOFTemplate] Failed! (endpoint){endpoint} (data){data}')
            return
        return data['data']

    def get_templates(self, fof_id, manager_id) -> 'list | None':
        # endpoint = '/v2/contract/getTemplateListByProduct'
        endpoint = '/v2/contract/getTemplateList'
        params = {'productId': fof_id}
        return self._request(endpoint, params, manager_id)

    def get_template_detail(self, template_id, manager_id) -> 'dict | None':
        endpoint = '/v2/contract/getContractTemplateInfo'
        params = {'contractTemplateId': template_id}
        return self._request(endpoint, params, manager_id)

    def get_contract_detail(self, contract_id, manager_id) -> 'dict | None':
        endpoint = '/v2/contract/getContractInfo'
        params = {'contractId': contract_id}
        return self._request(endpoint, params, manager_id)

    def save_fof_template(self, fof_id, manager_id):
        templates = self.get_templates(fof_id, manager_id)
        if not templates:
            return False

        for template in templates:
            template_type = HaiFengTemplateType.read(template['contractTemplateType'])
            if not template_type:
                continue

            ContractTemplate(
                template_id=template['contractTemplateId'],
                fof_id=fof_id,
                manager_id=manager_id,
                template_type=template_type,
            ).save(commit=False)

        db.session.commit()
        return True

    def get_template_download_url(self, template_id, manager_id) -> 'str | None':
        template_detail = self.get_template_detail(template_id, manager_id)
        if not template_detail:
            return
        return template_detail['downloadUrl']

    def get_contract_download_url(self, contract_id, manager_id) -> str:
        contract_detail = self.get_contract_detail(contract_id, manager_id)
        if not contract_detail:
            raise LogicError('获取合同文件失败!')
        return contract_detail['contractFileUrl']

