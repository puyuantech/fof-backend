from flask import request, g
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from utils.decorators import login_required
from utils.helper import generate_sql_pagination, replace_nan
from models import UnitMap
from models.from_surfing import HedgeFundInvestorPurAndRedemp, HedgeFundInvestorDivAndCarry, \
    HedgeFundInvestorPurAndRedempSub
from surfing.data.manager.manager_hedge_fund import HedgeFundDataManager


class TradesPurRedeemAPI(ApiViewHandler):
    """
    申赎交易记录
    """

    def add_investor_info(self, data_dict: dict):
        investor_id = data_dict.get('investor_id')
        unit_map = UnitMap.filter_by_query(
            investor_id=investor_id,
            manager_id=g.token.manager_id,
        ).first()
        if not unit_map:
            return data_dict

        sub = HedgeFundInvestorPurAndRedempSub.filter_by_query(
            main_id=data_dict.get('id'),
        ).first()
        if sub:
            data_dict['trade_confirm_url'] = sub.trade_confirm_url
            data_dict['trade_apply_url'] = sub.trade_apply_url
            data_dict['remark'] = sub.remark

        data_dict['investor_name'] = unit_map.name
        return data_dict

    @login_required
    def get(self):
        investor_id = request.args.get('investor_id')
        fof_id = request.args.get('fof_id')
        if not fof_id:
            raise VerifyError('No fof id')

        p = generate_sql_pagination()
        if investor_id:
            query = HedgeFundInvestorPurAndRedemp.filter_by_query(
                investor_id=investor_id,
                fof_id=fof_id,
            )
        else:
            query = HedgeFundInvestorPurAndRedemp.filter_by_query(
                fof_id=fof_id,
            )
        data = p.paginate(
            query,
            call_back=lambda x: [self.add_investor_info(i.to_dict()) for i in x],
            equal_filter=[HedgeFundInvestorPurAndRedemp.event_type]
        )
        return data

    @login_required
    def put(self):
        allow_columns = [
            "id",
            "fof_id",
            "datetime",
            "event_type",
            "investor_id",
            "net_asset_value",
            "acc_unit_value",
            "amount",
            "raising_interest",
            "redemp_share",
            "redemp_fee",
        ]
        data = {i: request.json.get(i) for i in allow_columns}
        HedgeFundDataManager().investor_pur_redemp_update(data)
        obj = HedgeFundInvestorPurAndRedempSub.filter_by_query(
            main_id=request.json.get('id'),
        ).first()
        if not obj:
            return

        update_columns = [
            'trade_confirm_url',
            'trade_apply_url',
            'remark',
        ]
        for i in update_columns:
            if request.json.get(i) is not None:
                obj.update(commit=False, **{i: request.json.get(i)})
        obj.save()

    @login_required
    def post(self):
        allow_columns = [
            "fof_id",
            "datetime",
            "event_type",
            "investor_id",
            "net_asset_value",
            "acc_unit_value",
            "amount",
            "raising_interest",
            "redemp_share",
            "redemp_fee",
        ]
        data = {i: request.json.get(i) for i in allow_columns}
        _id = HedgeFundDataManager().investor_pur_redemp_update(data)
        trade = HedgeFundInvestorPurAndRedempSub.create(
            main_id=_id,
            trade_confirm_url=request.json.get('trade_confirm_url'),
            trade_apply_url=request.json.get('trade_apply_url'),
            remark=request.json.get('remark'),
        )

        g.user_operation = '添加申赎交易记录'
        g.user_operation_params = {
            'fof_id': _id,
            'trade_id': trade.id,
        }

    @login_required
    def delete(self):
        _id = request.json.get('id')
        HedgeFundDataManager().investor_pur_redemp_remove(_id)


class TradesCarryEventAPI(ApiViewHandler):
    """
    计提事件
    """

    @login_required
    def post(self):
        df = HedgeFundDataManager().calc_carry_event(request.json)
        data = replace_nan(df.to_dict(orient='records'))
        for i in data:
            unit_map = UnitMap.filter_by_query(
                investor_id=i.get('investor_id'),
                manager_id=g.token.manager_id,
            ).first()
            if unit_map:
                i['investor_name'] = unit_map.name
        return data


class TradesDividendEventAPI(ApiViewHandler):
    """
    分红事件
    """

    @login_required
    def post(self):
        df = HedgeFundDataManager().calc_dividend_event(request.json)
        data = replace_nan(df.to_dict(orient='records'))
        for i in data:
            unit_map = UnitMap.filter_by_query(
                investor_id=i.get('investor_id'),
                manager_id=g.token.manager_id,
            ).first()
            if unit_map:
                i['investor_name'] = unit_map.name
        return data


class TradesDivAndCarryAPI(ApiViewHandler):
    """
    分红/计提交易记录
    """

    def add_investor_info(self, data_dict: dict):
        investor_id = data_dict.get('investor_id')
        unit_map = UnitMap.filter_by_query(
            investor_id=investor_id,
            manager_id=g.token.manager_id,
        ).first()
        if not unit_map:
            return data_dict

        data_dict['investor_name'] = unit_map.name
        return data_dict

    @login_required
    def get(self):
        investor_id = request.args.get('investor_id')
        fof_id = request.args.get('fof_id')
        if not fof_id:
            raise VerifyError('No fof id')

        p = generate_sql_pagination()
        if investor_id:
            query = HedgeFundInvestorDivAndCarry.filter_by_query(
                investor_id=investor_id,
                fof_id=fof_id,
            )
        else:
            query = HedgeFundInvestorDivAndCarry.filter_by_query(
                fof_id=fof_id,
            )
        data = p.paginate(
            query,
            call_back=lambda x: [self.add_investor_info(i.to_dict()) for i in x],
            equal_filter=[HedgeFundInvestorDivAndCarry.event_type],
        )
        return data

    @login_required
    def post(self):
        allow_columns = [
            "fof_id",
            "datetime",
            "event_type",
            "investor_id",
            "net_asset_value",
            "acc_unit_value",
            "total_dividend",
            "cash_dividend",
            "reinvest_amount",
            "carry_amount",
            "share_changed",
            "share_after_trans",
        ]
        data = {i: request.json.get(i) for i in allow_columns}
        HedgeFundDataManager().investor_div_carry_add(data)

        g.user_operation = '添加分红/计提记录'
        g.user_operation_params = {
            'fof_id': request.json.get('fof_id'),
        }

    @login_required
    def delete(self):
        _id = request.json.get('id')
        HedgeFundDataManager().investor_div_carry_remove(_id)

