from flask import request


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
    comments = [i.to_dict() for i in obj.comments]
    data.update({
        'comments': comments
    })
    return data

