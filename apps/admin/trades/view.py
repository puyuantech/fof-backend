
from flask import g, request
from models import FOFInfo, HedgeFundInvestorPurAndRedemp, HedgeFundInvestorDivAndCarry, \
    HedgeFundInvestorPurAndRedempSub, UnitMap
from bases.viewhandler import ApiViewHandler
from bases.globals import db
from utils.helper import generate_sql_pagination
from utils.decorators import login_required


class TradesPurRedAPI(ApiViewHandler):

    def add_investor_info(self, data_dict: dict):
        fof_id = data_dict.get('fof_id')
        fof = FOFInfo.filter_by_query(
            fof_id=fof_id,
            manager_id=g.token.manager_id,
        ).first()
        if not fof:
            return None

        investor_id = data_dict.get('investor_id')
        unit_map = UnitMap.filter_by_query(
            investor_id=investor_id,
            manager_id=g.token.manager_id,
        ).first()
        if unit_map:
            data_dict['investor_name'] = unit_map.name

        sub = HedgeFundInvestorPurAndRedempSub.filter_by_query(
            main_id=data_dict.get('id'),
        ).first()
        if sub:
            data_dict['trade_confirm_url'] = sub.trade_confirm_url
            data_dict['trade_apply_url'] = sub.trade_apply_url
            data_dict['remark'] = sub.remark

        data_dict['fof_name'] = fof.fof_name
        data_dict['desc_name'] = fof.desc_name
        data_dict['custodian_name'] = fof.custodian_name

        return data_dict

    @login_required
    def get(self):
        p = generate_sql_pagination()

        custodian_name = request.args.get('custodian_name')

        if custodian_name:
            fof = db.session.query(
                FOFInfo.fof_id,
            ).filter(
                FOFInfo.manager_id == g.token.manager_id,
                FOFInfo.custodian_name.contains(custodian_name),
                FOFInfo.is_deleted == False,
            ).all()
            fof_ids = [i[0] for i in fof]
        else:
            fof = db.session.query(
                FOFInfo.fof_id,
            ).filter(
                FOFInfo.manager_id == g.token.manager_id,
                FOFInfo.is_deleted == False,
            ).all()
            fof_ids = [i[0] for i in fof]

        query = db.session.query(
            HedgeFundInvestorPurAndRedemp
        ).filter(
            HedgeFundInvestorPurAndRedemp.manager_id == g.token.manager_id,
            HedgeFundInvestorPurAndRedemp.fof_id.in_(fof_ids),
        )
        data = p.paginate(
            query,
            call_back=lambda x: [self.add_investor_info(i.to_dict()) for i in x if self.add_investor_info(i.to_dict())],
            equal_filter=[
                HedgeFundInvestorPurAndRedemp.event_type,
                HedgeFundInvestorPurAndRedemp.fof_id,
                HedgeFundInvestorPurAndRedemp.investor_id,
            ],
        )
        return data


class TradesDivCarAPI(ApiViewHandler):

    def add_investor_info(self, data_dict: dict):
        fof_id = data_dict.get('fof_id')
        fof = FOFInfo.filter_by_query(
            fof_id=fof_id,
            manager_id=g.token.manager_id,
        ).first()
        if not fof:
            return None

        investor_id = data_dict.get('investor_id')
        unit_map = UnitMap.filter_by_query(
            investor_id=investor_id,
            manager_id=g.token.manager_id,
        ).first()
        if unit_map:
            data_dict['investor_name'] = unit_map.name

        data_dict['fof_name'] = fof.fof_name
        data_dict['desc_name'] = fof.desc_name
        data_dict['custodian_name'] = fof.custodian_name

        return data_dict

    @login_required
    def get(self):
        p = generate_sql_pagination()

        custodian_name = request.args.get('custodian_name')
        if custodian_name:
            fof = db.session.query(
                FOFInfo.fof_id,
            ).filter(
                FOFInfo.manager_id == g.token.manager_id,
                FOFInfo.custodian_name.contains(custodian_name),
                FOFInfo.is_deleted == False,
            ).all()
            fof_ids = [i[0] for i in fof]
        else:
            fof = db.session.query(
                FOFInfo.fof_id,
            ).filter(
                FOFInfo.manager_id == g.token.manager_id,
                FOFInfo.is_deleted == False,
            ).all()
            fof_ids = [i[0] for i in fof]

        query = db.session.query(
            HedgeFundInvestorDivAndCarry
        ).filter(
            HedgeFundInvestorDivAndCarry.manager_id == g.token.manager_id,
            HedgeFundInvestorDivAndCarry.fof_id.in_(fof_ids),
        )
        data = p.paginate(
            query,
            call_back=lambda x: [self.add_investor_info(i.to_dict()) for i in x if self.add_investor_info(i.to_dict())],
            equal_filter=[
                HedgeFundInvestorDivAndCarry.event_type,
                HedgeFundInvestorDivAndCarry.investor_id,
                HedgeFundInvestorDivAndCarry.fof_id,
            ],
        )
        return data
