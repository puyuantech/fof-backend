
from flask import g

from bases.constants import TemplateStatus
from bases.exceptions import LogicError
from bases.validation import ManagerValidation
from bases.viewhandler import ApiViewHandler
from extensions.haifeng.fof_template import FOFTemplate
from models import InvestorContract, FOFInfo, ProductionTemplate
from utils.decorators import login_required

from .validators.contract import FOFStartValidation


class ContractListAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = ManagerValidation.get_valid_data(self.input)
        investor_contracts = InvestorContract.get_manager_contracts(**data)

        fofs = FOFInfo.filter_by_query(manager_id=data['manager_id']).all()
        fofs = {fof.fof_id: fof.fof_name for fof in fofs}

        return [
            {
                'fof_name': fofs[investor_contract['fof_id']],
                **investor_contract
            }
            for investor_contract in investor_contracts
            if investor_contract['fof_id'] in fofs
        ]


class FOFListAPI(ApiViewHandler):

    @login_required
    def get(self):
        fofs = FOFInfo.filter_by_query(manager_id=g.token.manager_id).all()
        fofs = [
            {
                'fof_id': fof.fof_id,
                'fof_name': fof.fof_name,
            }
            for fof in fofs
        ]
        return ProductionTemplate.fill_template_status(g.token.manager_id, fofs)


class FOFStartAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FOFStartValidation.get_valid_data(self.input)
        production_template = ProductionTemplate.filter_by_query(manager_id=g.token.manager_id, **data).first()
        if production_template:
            raise LogicError('处理中！')

        production_template = ProductionTemplate.create(
            manager_id=g.token.manager_id,
            template_status=TemplateStatus.PROCESSING,
            **data,
        )
        if FOFTemplate(g.token.manager_id).save_fof_template(**data):
            production_template.update(template_status=TemplateStatus.SIGNING)
        return production_template.get_detail()


class FOFTemplatesAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = FOFStartValidation.get_valid_data(self.input)
        production_template = ProductionTemplate.get_by_query(manager_id=g.token.manager_id, **data)

        if production_template.template_status == TemplateStatus.PROCESSING and FOFTemplate(g.token.manager_id).save_fof_template(**data):
            production_template.update(template_status=TemplateStatus.SIGNING)
        return production_template.get_detail()

