
from bases.validation import ManagerValidation
from bases.viewhandler import ApiViewHandler
from models import InvestorContract, FOFInfo
from utils.decorators import login_required


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

