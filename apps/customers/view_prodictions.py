from flask import g

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from models import FOFInfo, FOFInvestorPosition


class CusProductions(ApiViewHandler):

    @login_required
    def get(self, investor_id):
        productions = FOFInfo.filter_by_query(
            manager_id=g.token.manager_id,
            is_on_sale=True,
        ).all()

        results = db.session.query(FOFInfo).filter(
            FOFInvestorPosition.investor_id == investor_id,
            FOFInvestorPosition.manager_id == g.token.manager_id,
            FOFInfo.fof_id == FOFInvestorPosition.fof_id,
            FOFInfo.is_deleted == False,
            FOFInfo.manager_id == g.token.manager_id,
        ).all()

        productions = {i.fof_id: i for i in productions}
        results = {i.fof_id: i for i in results}

        data = []
        for i in results:
            if i not in productions:
                data.append(results[i])

        for i in productions:
            data.append(i)

        data = [i.to_dict() for i in data]
        return data

