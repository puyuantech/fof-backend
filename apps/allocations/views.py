from flask import request

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import HedgeAllocation, HedgeFundInfo
from utils.decorators import params_required, login_required
from utils.helper import generate_sql_pagination, replace_nan

from .libs import make_hedge_favorite_info


class AllocationAPI(ApiViewHandler):

    @login_required
    def get(self):
        fof_id = request.args.get('fof_id')
        p = generate_sql_pagination()
        query = db.session.query(
            HedgeAllocation
        ).filter(
            HedgeAllocation.fof_id == fof_id,
            HedgeAllocation.is_deleted == False,
        )
        data = p.paginate(query, call_back=lambda x: [make_hedge_favorite_info(i) for i in x])

        return data

    @login_required
    @params_required(*['fund_id', 'fof_id'])
    def post(self):
        obj = HedgeAllocation.filter_by_query(
            fof_id=self.input.fof_id,
            fund_id=self.input.fund_id,
        ).one_or_none()
        if obj:
            return

        HedgeAllocation.create(
            fof_id=self.input.fof_id,
            fund_id=self.input.fund_id,
        )

    @params_required(*['fund_id', 'fof_id'])
    @login_required
    def delete(self):
        obj = HedgeAllocation.filter_by_query(
            fof_id=self.input.fof_id,
            fund_id=self.input.fund_id,
        ).one_or_none()
        if not obj:
            return
        obj.logic_delete()


class AllocationStatusAPI(ApiViewHandler):

    @login_required
    def get(self):
        fund_id = request.args.get('fund_id')
        fof_id = request.args.get('fof_id')
        if not fund_id:
            raise VerifyError('参数错误')

        obj = HedgeAllocation.filter_by_query(
            fof_id=fof_id,
            fund_id=fund_id,
        ).one_or_none()
        if obj:
            return {
                'status': True,
            }
        return {
                'status': False,
            }

