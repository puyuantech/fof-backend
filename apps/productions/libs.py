from flask import request


def update_production_info(obj):
    columns = [
        'datetime',
        'fof_name',
        'admin',
        'established_date',
        'fof_status',
        'subscription_fee',
        'redemption_fee',
        'management_fee',
        'custodian_fee',
        'administrative_fee',
        'lock_up_period',
        'incentive_fee_mode',
        'incentive_fee',
        'current_deposit_rate',
        'initial_raised_fv',
        'initial_net_value',
    ]
    for i in columns:
        if request.json.get(i) is not None:
            obj.update(commit=False, **{i: request.json.get(i)})
    obj.save()
    return obj

