from flask import request, g
from bases.globals import db
from models import HedgeFundInfo, HedgeFundNAV, HedgeComment, HedgeFavorite, HedgeAllocation


def update_hedge_fund_info(obj):
    columns = [
        'fund_name',
        'manager_id',
        'manager',
        'water_line',
        'incentive_fee_mode',
        'incentive_fee_ratio',
        'v_nav_decimals',
        'brief_name',
        'stars',
        'comment',
        'company',
        'found_date',
        'invest_strategy',
        'incentive_fee_type',
        'incentive_fee_str',
        'size',
        'manager',
        'incentive_fee_date',
        'fund_adviser',
        'records_no',
        'records_date',
        'deposit_security',
        'open_date',
        'warning_line',
        'closeout_line',
        'management_fee',
        'custodian_fee',
        'administrative_fee',
        'purchase_fee',
        'redeem_fee',
        'purchase_confirmed',
        'purchase_done',
        'redeem_confirmed',
        'redeem_done',

    ]
    for i in columns:
        if request.json.get(i) is not None:
            obj.update(commit=False, **{i: request.json.get(i)})
    obj.save()
    return obj


def make_hedge_fund_info(obj):
    data = obj.to_dict()
    comments = HedgeComment.filter_by_query(fund_id=obj.fund_id).all()
    favorite = HedgeFavorite.filter_by_query(
        fund_id=obj.fund_id,
        user_id=g.user.id,
    ).one_or_none()
    comments = [i.to_dict() for i in comments]
    data.update({
        'comments': comments,
        'favorite_status': True if favorite else False,
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
    info.adjusted_net_value = nav.adjusted_net_value
    db.session.commit()

