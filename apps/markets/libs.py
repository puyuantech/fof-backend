from flask import request


def update_custom_index_info(obj):
    columns = [
        'name',
        'desc',
    ]
    for i in columns:
        if request.json.get(i) is not None:
            obj.update(commit=False, **{i: request.json.get(i)})
    obj.save()
    return obj


def update_custom_index_ratios(obj, ratios):
    obj.recent_1m_ret = float(ratios.recent_1m_ret)
    obj.recent_3m_ret = float(ratios.recent_3m_ret)
    obj.recent_6m_ret = float(ratios.recent_6m_ret)
    obj.recent_y1_ret = float(ratios.recent_y1_ret)
    obj.recent_y3_ret = float(ratios.recent_y3_ret)
    obj.recent_y5_ret = float(ratios.recent_y5_ret)
    obj.mdd = float(ratios.mdd)
    obj.sharpe = float(ratios.sharpe)
    obj.last_unit_nav = float(ratios.last_unit_nav)
    obj.annualized_ret = float(ratios.annualized_ret)
    obj.annualized_vol = float(ratios.annualized_vol)
    obj.start_date = ratios.start_date
    obj.end_date = ratios.end_date
    return obj

