import pandas as pd
import datetime
import traceback
import io
from flask import request, current_app

from bases.exceptions import VerifyError, LogicError
from models import FOFAssetAllocation, FOFNav
from utils.caches import get_fund_collection_caches
from surfing.constant import FOFStatementStatus, FOFTradeStatus, FOFTransitStatus, FOFOtherRecordStatus


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
        'incentive_fee_type',
        'incentive_fee_str',
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


def parse_investor_trade_file(fof_id):
    req_file = request.files.get('file')
    if not req_file:
        raise VerifyError('Couldn\'t find any uploaded file')

    # 解析文件
    try:
        df = pd.read_excel(
            io.BytesIO(req_file.read()),
            dtype={'日期': str},
        )

        df = df[['日期', '用户ID', '申购金额', '赎回份额', '确认日期', '入账日期', '确认份额']]
        df = df.rename(columns={
            '日期': 'datetime',
            '用户ID': 'investor_id',
            '申购金额': 'amount',
            '赎回份额': 'share',
            '确认日期': 'confirmed_date',
            '入账日期': 'deposited_date',
            '确认份额': 'unit_total',
        })
        df['asset_type'] = 2
        df['fof_id'] = fof_id
    except:
        current_app.logger.error(traceback.format_exc())
        raise VerifyError('解析失败')

    return df


def parse_nav_file(fof_id):
    req_file = request.files.get('file')
    if not req_file:
        raise VerifyError('Couldn\'t find any uploaded file')

    # 解析文件
    try:
        df = pd.read_excel(
            io.BytesIO(req_file.read()),
            dtype={'日期': str},
        )
        df = df.dropna(how='all')

        df = df[['日期', '净值', '总份额', '投资成本', '当前市值', '累计收益', '累计收益率']]
        df['日期'] = df['日期'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())
        df = df.rename(columns={
            '日期': 'datetime',
            '净值': 'nav',
            '总份额': 'volume',
            '投资成本': 'cost',
            '当前市值': 'mv',
            '累计收益': 'income',
            '累计收益率': 'income_rate',
        })
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
            nav=request.json.get('nav'),
            event_type=request.json.get('event_type'),
            status=request.json.get('status'),
            confirmed_date=request.json.get('confirmed_date'),
            unit_total=request.json.get('unit_total'),
        )
    except:
        current_app.logger.error(traceback.format_exc())
        raise VerifyError('创建失败！')


def create_single_nav(fof_id, date):
    try:
        FOFNav.create(
            fof_id=fof_id,
            datetime=date,
            nav=request.json.get('nav'),
            acc_net_value=request.json.get('nav'),
            volume=request.json.get('volume'),
            mv=request.json.get('mv'),
            ret=request.json.get('ret'),
        )
    except:
        current_app.logger.error(traceback.format_exc())
        raise LogicError('创建失败！')


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
        'event_type',
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


def update_nav(obj):
    columns = [
        'nav',
        'volume',
        'acc_net_value',
        'mv',
        'ret',
    ]

    for i in columns:
        if request.json.get(i) is not None:
            obj.update(commit=False, **{i: request.json.get(i)})
    obj.save()
    return obj


def update_account_statement(self, obj):
    columns = [
        'datetime',
        'trade_num',
        'event_type',
        'amount',
        'remain_cash',
        'remark',
    ]

    for i in columns:
        if request.json.get(i) is not None:
            obj.update(commit=False, **{i: request.json.get(i)})
    obj.save()
    return obj


def parse_account_statement(self, fof_id):
    req_file = request.files.get('file')
    if not req_file:
        raise VerifyError('Couldn\'t find any uploaded file')

    # 解析文件
    try:
        df = pd.read_excel(
            io.BytesIO(req_file.read()),
            dtype={'时间': str},
        )
        df = df.dropna(how='all')

        df = df[['时间', '流水编号', '交易类型', '金额', '账户余额', '备注']]
        df['日期'] = df['日期'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())
        df = df.rename(columns={
            '时间': 'datetime',
            '流水编号': 'trade_num',
            '交易类型': 'event_type',
            '金额': 'amount',
            '账户余额': 'remain_cash',
            '备注': 'remark',
        })
        df['fof_id'] = fof_id
    except:
        current_app.logger.error(traceback.format_exc())
        raise VerifyError('解析失败')

    return df


def update_transit_money(self, obj):
    columns = [
        'fund_id',
        'confirmed_datetime',
        'event_type',
        'amount',
        'transit_cash',
        'remark',
    ]

    for i in columns:
        if request.json.get(i) is not None:
            obj.update(commit=False, **{i: request.json.get(i)})
    obj.save()
    return obj


def update_incidental_statement(self, obj):
    columns = [
        'datetime',
        'trade_num',
        'event_type',
        'amount',
        'remark',
    ]

    for i in columns:
        if request.json.get(i) is not None:
            obj.update(commit=False, **{i: request.json.get(i)})
    obj.save()
    return obj


def parse_transit_money(self, fof_id):
    req_file = request.files.get('file')
    if not req_file:
        raise VerifyError('Couldn\'t find any uploaded file')

    # 解析文件
    try:
        df = pd.read_excel(
            io.BytesIO(req_file.read()),
            dtype={'时间': str},
        )
        df = df.dropna(how='all')

        df = df[['基金ID', '确认时间', '类型', '金额', '在途资金总额', '备注']]
        df['日期'] = df['日期'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())
        df = df.rename(columns={
            '基金ID': 'fund_id',
            '确认时间': 'confirmed_datetime',
            '类型': 'event_type',
            '金额': 'amount',
            '在途资金总额': 'transit_cash',
            '备注': 'remark',
        })
        df['fof_id'] = fof_id
    except:
        current_app.logger.error(traceback.format_exc())
        raise VerifyError('解析失败')

    return df


def update_estimate_interest(self, obj):
    columns = [
        'date',
        'remain_cash',
        'interest',
        'remark',
        'total_interest',
    ]

    for i in columns:
        if request.json.get(i) is not None:
            obj.update(commit=False, **{i: request.json.get(i)})
    obj.save()
    return obj


def update_estimate_fee(self, obj):
    columns = [
        'date',
        'pre_market_value',
        'management_fee',
        'total_management_fee',
        'custodian_fee',
        'total_custodian_fee',
        'administrative_fee',
        'total_administrative_fee',
        'is_down',
        'remark',
    ]

    for i in columns:
        if request.json.get(i) is not None:
            obj.update(commit=False, **{i: request.json.get(i)})
    obj.save()
    return obj


def update_other_record(self, obj):
    columns = [
        'event_type',
        'amount',
        'remark',
        'date',
    ]

    for i in columns:
        if request.json.get(i) is not None:
            obj.update(commit=False, **{i: request.json.get(i)})
    obj.save()
    return obj

