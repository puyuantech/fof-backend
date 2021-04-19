from flask import g, request
from bases.viewhandler import ApiViewHandler
from bases.constants import StuffEnum
from bases.globals import db
from utils.decorators import admin_login_required, login_required, params_required
from utils.helper import generate_sql_pagination
from models import Operation, User, InvestorOperation, UnitMap

from sqlalchemy import distinct


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


class OperationsListAPI(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def get(self):
        results = db.session.query(distinct(Operation.action)).all()
        data = [i[0] for i in results]
        return data


class InvestorOperationAPI(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def get(self):
        p = generate_sql_pagination()

        query = InvestorOperation.filter_by_query(
            manager_id=g.token.manager_id,
        )
        data = p.paginate(
            query,
            equal_filter=[Operation.user_id, Operation.action, Operation.investor_id],
            range_filter=[Operation.create_time],
        )

        for i in data['results']:
            u = UnitMap.filter_by_query(
                investor_id=i['investor_id'],
                manager_id=g.token.manager_id,
            ).first()
            if u:
                i['mobile'] = u.mobile
                i['name'] = u.name
        return data

    @params_required(*['request_data', 'investor_id', 'action'])
    @login_required
    def post(self):
        remote_addr = request.headers.get('X-Real-Ip') if request.headers.get('X-Real-Ip') else '0.0.0.0'
        InvestorOperation.create(
            investor_id=self.input.investor_id,
            user_id=g.user.id,
            manager_id=g.token.manager_id,
            ip=str(remote_addr),
            action=self.input.action,
            url=str(request.url),
            method=request.method,
            request_data=self.input.request_data,
            response_data='',
            response_status=None,
        )
