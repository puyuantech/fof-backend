
from bases.validation import ManagerValidation
from bases.viewhandler import ApiViewHandler
from extensions.haifeng.haifeng_token import HaiFengToken
from models import InvestorCertification
from utils.decorators import login_required
from utils.helper import generate_sql_pagination


class CertificationListAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = ManagerValidation.get_valid_data(self.input)

        p = generate_sql_pagination()
        query = InvestorCertification.filter_by_query(**data, is_latest=True)
        return p.paginate(query, call_back=lambda x: [i.get_investor_certification() for i in x])

