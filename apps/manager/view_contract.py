
from flask import g

from bases.constants import TemplateStatus
from bases.exceptions import LogicError
from bases.viewhandler import ApiViewHandler
from extensions.haifeng.fof_template import FOFTemplate
from models import InvestorContract, FOFInfo, ProductionSignStatus
from utils.decorators import login_required

from .validators.contract import FOFStartValidation


class ContractListAPI(ApiViewHandler):

    @login_required
    def get(self):
        investor_contracts = InvestorContract.get_manager_contracts(g.token.manager_id)

        fofs = FOFInfo.filter_by_query(manager_id=g.token.manager_id).all()
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
                'desc_name': fof.desc_name,
            }
            for fof in fofs
        ]
        return ProductionSignStatus.fill_template_status(g.token.manager_id, fofs)


class FOFStartAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = FOFStartValidation.get_valid_data(self.input)
        production_template = ProductionSignStatus.filter_by_query(manager_id=g.token.manager_id, **data).first()
        if production_template:
            raise LogicError('处理中！')

        production_template = ProductionSignStatus.create(
            manager_id=g.token.manager_id,
            template_status=TemplateStatus.PROCESSING,
            **data,
        )
        if FOFTemplate().save_fof_template(g.token.manager_id, **data):
            production_template.update(template_status=TemplateStatus.SIGNING)
        return production_template.get_detail()


class FOFTemplatesAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = FOFStartValidation.get_valid_data(self.input)
        production_template = ProductionSignStatus.get_by_query(manager_id=g.token.manager_id, **data)

        if production_template.template_status == TemplateStatus.PROCESSING and FOFTemplate().save_fof_template(g.token.manager_id, **data):
            production_template.update(template_status=TemplateStatus.SIGNING)
        return production_template.get_detail()

