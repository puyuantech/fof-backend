from flask import g
from bases.viewhandler import ApiViewHandler
from bases.constants import StuffEnum
from utils.decorators import admin_login_required
from utils.helper import generate_sql_pagination
from models import Operation, User


class OperationsAPI(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def get(self):
        p = generate_sql_pagination()

        query = Operation.filter_by_query(
            manager_id=g.token.manager_id,
        )
        data = p.paginate(
            query,
            equal_filter=[Operation.user_id, Operation.action],
            range_filter=[Operation.create_time],
        )

        for i in data['results']:
            u = User.filter_by_query(id=i['user_id']).first()
            if u:
                i['username'] = u.username
        return data
