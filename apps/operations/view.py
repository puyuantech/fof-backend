from flask import g
from bases.viewhandler import ApiViewHandler
from bases.constants import StuffEnum
from utils.decorators import admin_login_required
from utils.helper import generate_sql_pagination
from models import Operation


class OperationsAPI(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def get(self):
        p = generate_sql_pagination()

        query = Operation.filter_by_query(
            manager_id=g.token.manager_id,
        )
        data = p.paginate(query)
        return data
