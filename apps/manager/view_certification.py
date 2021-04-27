
from flask import g

from bases.viewhandler import ApiViewHandler
from models import InvestorCertification
from utils.decorators import login_required
from utils.helper import generate_sql_pagination


class CertificationListAPI(ApiViewHandler):

    @login_required
    def get(self):
        p = generate_sql_pagination()
        query = InvestorCertification.filter_by_query(manager_id=g.token.manager_id, is_latest=True)
        return p.paginate(query, call_back=lambda x: [i.get_investor_certification() for i in x])

