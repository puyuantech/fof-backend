from flask import g, request

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import HedgeFavorite, HedgeFundInfo
from utils.decorators import params_required, login_required
from utils.helper import generate_sql_pagination, replace_nan

from .libs import make_hedge_favorite_info


class FavoriteAPI(ApiViewHandler):

    @login_required
    def get(self):
        p = generate_sql_pagination()
        query = db.session.query(
            HedgeFavorite
        ).filter(
            HedgeFavorite.user_id == g.user.id,
            HedgeFavorite.is_deleted == False,
        )
        data = p.paginate(query, call_back=lambda x: [make_hedge_favorite_info(i) for i in x])

        return data

    @login_required
    @params_required(*['fund_id'])
    def post(self):
        obj = HedgeFavorite.filter_by_query(
            user_id=g.user.id,
            fund_id=self.input.fund_id,
        ).one_or_none()
        if obj:
            return
        HedgeFavorite.create(
            user_id=g.user.id,
            fund_id=self.input.fund_id,
        )

    @login_required
    @params_required(*['fund_id'])
    def delete(self):
        obj = HedgeFavorite.filter_by_query(
            user_id=g.user.id,
            fund_id=self.input.fund_id,
        ).one_or_none()
        if not obj:
            return
        obj.logic_delete()


class FavoriteDetailAPI(ApiViewHandler):
    @login_required
    def get(self, _id):
        obj = HedgeFavorite.get_by_id(_id)
        data = make_hedge_favorite_info(obj)
        return replace_nan(data)


class FavoriteStatusAPI(ApiViewHandler):

    @login_required
    def get(self):
        fund_id = request.args.get('fund_id')
        if not fund_id:
            raise VerifyError('参数错误')

        hedge = HedgeFundInfo.get_by_query(
            fund_id=fund_id,
        ).one_or_none()
        if not hedge:
            raise VerifyError('基金不存在')

        obj = HedgeFavorite.filter_by_query(
            fund_id=fund_id,
            user_id=g.user.id
        ).one_or_none()
        if obj:
            return {
                'status': True,
            }

        return {
                'status': False,
            }

