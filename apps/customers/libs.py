import datetime
import traceback
import pandas as pd
import io
from flask import request, current_app

from models import User, FOFScaleAlteration, FOFInvestorData, InvestorTag, InvestorInfo
from bases.exceptions import VerifyError
from bases.constants import StuffEnum


def get_user_by_username(username):
    return User.filter_by_query(username=username).first()


def get_user_by_mobile(mobile):
    return User.filter_by_query(mobile=mobile).first()


def get_investor_info(unit):
    data_dict = unit.to_cus_dict()

    tags = InvestorTag.filter_by_query(
        investor_id=unit.investor_id,
        manager_id=unit.manager_id,
    ).all()
    if not tags:
        data_dict['tags'] = []
    else:
        data_dict['tags'] = [i.to_dict() for i in tags]

    investor_data = FOFInvestorData.filter_by_query(
        investor_id=unit.investor_id,
    ).first()
    if not investor_data:
        data_dict['total_investment'] = None
    else:
        data_dict['total_investment'] = investor_data.total_investment

    return data_dict


def register_investor_user(mobile):
    investor = InvestorInfo.get_by_mobile(mobile)

    if investor.check_manager_map(mobile):
        raise VerifyError('此手机号已添加过')

    if not investor:
        user, investor = User.create_main_user_investor(mobile)

    unit_map = investor.create_manager_map(g.token.manager_id)
    return unit_map


def check_investor_id(user, investor_id):
    if user.investor_id == investor_id:
        return
    if User.filter_by_query(investor_id=request.json.get('investor_id')).first():
        raise VerifyError('投资者ID已存在')


def check_user_mobile(user, mobile):
    if user.mobile == mobile:
        return
    if User.filter_by_query(mobile=request.json.get('mobile')).first():
        raise VerifyError('电话号码已存在')


def update_user_info(user):
    columns = [
        'nick_name',
        'sex',
        'email',
        'mobile',
        'avatar_url',
        'site',
        'name',
        'amount',
        'sign_date',
        'sponsor',
        'investor_id',
        'cred',
        'cred_type',
        'is_institution',
        'address',
        'ins_name',
        'ins_code',
        'contact_name',
        'contact_mobile',
        'status',
        'origin',
        'salesman',
    ]

    if request.json.get('investor_id'):
        check_investor_id(user, request.json.get('investor_id'))

    if request.json.get('mobile'):
        check_user_mobile(user, request.json.get('mobile'))

    for i in columns:
        if request.json.get(i) is not None:
            user.update(commit=False, **{i: request.json.get(i)})
    user.save()
    return user


def parse_trade_file(investor_id):
    req_file = request.files.get('file')
    if not req_file:
        raise VerifyError('Couldn\'t find any uploaded file')

    # 解析文件
    try:
        df = pd.read_excel(
            io.BytesIO(req_file.read()),
            dtype={'日期': str, '产品ID': str},
        )

        df = df[['日期', '产品ID', '申购金额', '赎回份额', '确认日期', '入账日期', '确认份额']]
        # df['日期'] = df['日期'].apply(lambda x: datetime.datetime.strptime(x[10], '%Y-%m-%d').date())
        df = df.rename(columns={
            '日期': 'datetime',
            '产品ID': 'fof_id',
            '申购金额': 'amount',
            '赎回份额': 'share',
            '确认日期': 'confirmed_date',
            '入账日期': 'deposited_date',
            '确认份额': 'unit_total',
        })
        df['asset_type'] = 2
        df['investor_id'] = investor_id
    except:
        current_app.logger.error(traceback.format_exc())
        raise VerifyError('解析失败')

    return df


def create_single_trade(investor_id):
    try:
        FOFScaleAlteration.create(
            fof_id=request.json.get('fof_id'),
            datetime=request.json.get('datetime'),
            investor_id=request.json.get('investor_id'),
            applied_date=request.json.get('applied_date'),
            deposited_date=request.json.get('deposited_date'),
            amount=request.json.get('amount'),
            share=request.json.get('share'),
            event_type=request.json.get('event_type'),
            asset_type=request.json.get('asset_type', 2),
            status=request.json.get('status'),
            nav=request.json.get('nav'),
            manager_id=g.token.manager_id,
        )
    except:
        current_app.logger.error(traceback.format_exc())
        raise VerifyError('创建失败！')


def update_trade(obj):
    columns = [
        'datetime',
        'fof_id',
        'investor_id',
        'applied_date',
        'deposited_date',
        'amount',
        'share',
        'event_type',
        'asset_type',
        'status',
        'nav',
    ]
    for i in columns:
        if request.json.get(i) is not None:
            obj.update(commit=False, **{i: request.json.get(i)})
    obj.save()
    return obj

