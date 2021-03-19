from flask import request, g
from bases.viewhandler import ApiViewHandler
from bases.globals import db
from bases.exceptions import VerifyError
from utils.decorators import login_required
from utils.helper import generate_sql_pagination
from models.from_surfing import HedgeFundInvestorPurAndRedemp, HedgeFundInvestorDivAndCarry
from surfing.data.manager.manager_hedge_fund import HedgeFundDataManager


class TradesPurRedeemAPI(ApiViewHandler):
    """
    申赎交易记录
    """

    @login_required
    def get(self):
        investor_id = request.args.get('investor_id')
        if not investor_id:
            raise VerifyError('No investor id')

        fof_id = request.args.get('fof_id')
        if not fof_id:
            raise VerifyError('No fof id')

        p = generate_sql_pagination()
        query = HedgeFundInvestorPurAndRedemp.filter_by_query(
            investor_id=investor_id,
            fof_id=fof_id,
        )
        data = p.paginate(query)
        return data

    @login_required
    def put(self):
        data = request.json
        HedgeFundDataManager().investor_pur_redemp_update(data)

    @login_required
    def post(self):
        data = request.json
        HedgeFundDataManager().investor_pur_redemp_update(data)

    @login_required
    def delete(self):
        _id = request.json.get('id')
        HedgeFundDataManager().investor_pur_redemp_remove(_id)


class TradesCarryEventAPI(ApiViewHandler):
    """
    计提事件
    """

    @login_required
    def get(self):
        df = HedgeFundDataManager().calc_carry_event(request.json)
        return df.to_dict(orient='r')


class TradesDividendEventAPI(ApiViewHandler):
    """
    分红事件
    """

    @login_required
    def get(self):
        df = HedgeFundDataManager().calc_dividend_event(request.json)
        return df.to_dict(orient='r')


class TradesDivAndCarryAPI(ApiViewHandler):
    """
    分红/计提交易记录
    """

    @login_required
    def get(self):
        investor_id = request.args.get('investor_id')
        if not investor_id:
            raise VerifyError('No investor id')

        fof_id = request.args.get('fof_id')
        if not fof_id:
            raise VerifyError('No fof id')

        p = generate_sql_pagination()
        query = HedgeFundInvestorDivAndCarry.filter_by_query(
            investor_id=investor_id,
            fof_id=fof_id,
        )
        data = p.paginate(query)
        return data

    @login_required
    def post(self):
        data = request.json
        HedgeFundDataManager().investor_div_carry_add(data)

    @login_required
    def delete(self):
        _id = request.json.get('id')
        HedgeFundDataManager().investor_div_carry_remove(_id)

