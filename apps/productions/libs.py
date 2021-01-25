import pandas as pd
import datetime
import traceback
import io
from flask import request, current_app

from bases.exceptions import VerifyError
from models import FOFAssetAllocation
from utils.caches import get_fund_collection_caches
from surfing.constant import HoldingAssetType, FundStatus


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


def get_asset_type_by_fund(fund_id):
    fund_df = get_fund_collection_caches()
    asset_type = 1 if fund_id in fund_df.index else 2
    return asset_type


def parse_status(x):
    if x == '完成':
        return 1

    if x == '在途':
        return 2

    if x == '计提完成':
        return 3

    return


def parse_trade_file(fof_id):
    req_file = request.files.get('file')
    if not req_file:
        raise VerifyError('Couldn\'t find any uploaded file')

    # 解析文件
    try:
        df = pd.read_excel(
            io.BytesIO(req_file.read()),
            dtype={'日期': str, '基金ID': str},
        )
        df = df.dropna(how='all')

        df = df[['日期', '基金ID', '申购金额', '赎回份额', '状态', '确认日期', '确认份额']]
        df['日期'] = df['日期'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())
        df = df.rename(columns={
            '日期': 'datetime',
            '基金ID': 'fund_id',
            '申购金额': 'amount',
            '赎回份额': 'share',
            '状态': 'status',
            '确认日期': 'confirmed_date',
            '确认份额': 'unit_total',
        })
        df['asset_type'] = df['fund_id'].apply(get_asset_type_by_fund)
        df['status'] = df['status'].apply(parse_status)
        df['fof_id'] = fof_id
        print(df)
    except:
        current_app.logger.error(traceback.format_exc())
        raise VerifyError('解析失败')

    return df


def create_single_trade(fof_id):
    try:
        fund_id = request.json.get('fund_id')
        asset_type = get_asset_type_by_fund(fund_id)

        FOFAssetAllocation.create(
            fof_id=fof_id,
            datetime=request.json.get('datetime'),
            fund_id=request.json.get('fund_id'),
            asset_type=asset_type,
            amount=request.json.get('amount'),
            share=request.json.get('share'),
            status=request.json.get('status'),
            confirmed_date=request.json.get('confirmed_date'),
            unit_total=request.json.get('unit_total'),
        )
    except:
        current_app.logger.error(traceback.format_exc())
        raise VerifyError('创建失败！')


def update_trade(obj):
    columns = [
        'datetime',
        'fund_id',
        'amount',
        'share',
        'status',
        'amount',
        'confirmed_date',
        'unit_total',
    ]
    if request.json.get('fund_id'):
        fund_id = request.json.get('fund_id')
        asset_type = get_asset_type_by_fund(fund_id)
        obj.asset_type = asset_type

    for i in columns:
        if request.json.get(i) is not None:
            obj.update(commit=False, **{i: request.json.get(i)})
    obj.save()
    return obj

