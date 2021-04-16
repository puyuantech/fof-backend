
import pandas as pd

from flask import g

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from models import FOFInfo, FOFInvestorPosition, FOFInvestorPositionSummary, HedgeFundInvestorDivAndCarry, HedgeFundInvestorPurAndRedemp
from utils.decorators import login_required
from utils.helper import replace_nan

from .libs import get_monthly


class PositionListAPI(ApiViewHandler):

    @login_required
    def get(self):
        results = db.session.query(FOFInvestorPosition, FOFInfo).filter(
            FOFInvestorPosition.investor_id == g.token.investor_id,
            FOFInvestorPosition.manager_id == g.token.manager_id,
            FOFInfo.fof_id == FOFInvestorPosition.fof_id,
            FOFInfo.is_deleted == False,
            FOFInfo.manager_id == g.token.manager_id,
        ).all()

        df_data = []
        for position, info in results:
            df_data.append({
                'fof_id': position.fof_id,
                'datetime': position.datetime,
                'mv': position.mv,
                'total_ret': position.total_ret,
                'fof_name': info.fof_name,
                'desc_name': info.desc_name,
            })

        df = pd.DataFrame(df_data)

        if len(df) < 1:
            return []

        df['sum_total_ret'] = df['total_ret'].sum()
        df['sum_mv'] = df['mv'].sum()
        df['weight'] = df['mv'] / df['sum_mv']
        return replace_nan(df.to_dict(orient='records'))


class PositionAnalysisAPI(ApiViewHandler):

    @login_required
    def get(self):
        results = FOFInvestorPositionSummary.filter_by_query(
            investor_id=g.token.investor_id,
            manager_id=g.token.manager_id,
        ).order_by(
            FOFInvestorPositionSummary.datetime.asc(),
        ).all()
        data = {
            'dates': [],
            '总资产': [],
            '累计收益': [],
            '累计收益率': [],
        }
        for i in results:
            data['总资产'].append(i.mv)
            data['累计收益'].append(i.total_ret)
            data['累计收益率'].append(i.total_rr)
            data['dates'].append(i.datetime)

        pur_redemps = HedgeFundInvestorPurAndRedemp.filter_by_query(
            investor_id=g.token.investor_id,
            manager_id=g.token.manager_id,
        ).all()

        div_carrys = HedgeFundInvestorDivAndCarry.filter_by_query(
            investor_id=g.token.investor_id,
            manager_id=g.token.manager_id,
        ).all()

        return replace_nan({
            'history': data,
            'monthly': get_monthly(data['dates'], data['总资产']),
            'pur_redemps': [pur_redemp.to_dict() for pur_redemp in pur_redemps],
            'div_carrys': [div_carry.to_dict() for div_carry in div_carrys],
        })

