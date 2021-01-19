from flask import request
from bases.globals import db
from models import HedgeFundInfo, HedgeFundNAV, HedgeComment


def update_hedge_fund_info(obj):
    columns = [
        'fund_name',
        'manager_id',
        'manager',
        'water_line',
        'incentive_fee_mode',
        'incentive_fee_ratio',
        'v_nav_decimals',
        'stars',
        'comment',
    ]
    for i in columns:
        if request.json.get(i) is not None:
            obj.update(commit=False, **{i: request.json.get(i)})
    obj.save()
    return obj


def make_hedge_fund_info(obj):
    data = obj.to_dict()
    comments = HedgeComment.filter_by_query(fund_id=obj.fund_id).all()
    comments = [i.to_dict() for i in comments]
    data.update({
        'comments': comments
    })
    return data


def update_hedge_value(fund_id):
    """
    保存最新的值到info里
    :param fund_id:
    :return:
    """
    info = HedgeFundInfo.get_by_query(fund_id=fund_id)
    nav = db.session.query(HedgeFundNAV).filter(
        HedgeFundNAV.fund_id == fund_id,
    ).order_by(HedgeFundNAV.datetime.desc()).first()
    if not nav:
        return

    info.net_asset_value = nav.net_asset_value
    info.acc_unit_value = nav.acc_unit_value
    info.v_net_value = nav.v_net_value
    db.session.commit()

