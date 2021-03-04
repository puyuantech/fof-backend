from flask import request
from models import InfoToProduction, FOFInfo
from bases.globals import db


def get_info_production(obj):
    data_dict = obj.to_dict()

    items = InfoToProduction.filter_by_query(
        info_id=obj.id,
    ).all()
    fof_ids = [i.fof_id for i in items]

    productions = db.session.query(
        FOFInfo.fof_name,
        FOFInfo.fof_id,
    ).filter(
        FOFInfo.fof_id.in_(fof_ids)
    ).all()

    productions = [
        {
            'fof_id': i[1],
            'fof_name': i[0],
        }
        for i in productions
    ]
    data_dict['productions'] = productions
    return data_dict


def update_info_production(obj):
    productions = request.json.get('productions')
    if not productions:
        return

    items = InfoToProduction.filter_by_query(
        info_id=obj.id,
    ).all()
    fof_ids = [i.fof_id for i in items]

    for i in fof_ids:
        if i not in productions:
            i.logic_delete()

    for i in productions:
        if i not in fof_ids:
            InfoToProduction.create(
                fof_id=i,
                info_id=obj.id,
            )
