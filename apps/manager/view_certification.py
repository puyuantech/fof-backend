
from bases.validation import ManagerValidation
from bases.viewhandler import ApiViewHandler
from extensions.haifeng.manager_token import ManagerToken
from models import InvestorCertification
from utils.decorators import login_required


class CertificationTokenAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = ManagerValidation.get_valid_data(self.input)
        return ManagerToken().get_uid_and_token(**data)


class CertificationListAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = ManagerValidation.get_valid_data(self.input)
        investors = InvestorCertification.filter_by_query(**data, is_latest=True).all()
        return [investor.get_investor_certification() for investor in investors]

