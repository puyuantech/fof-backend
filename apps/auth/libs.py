import datetime
import traceback
from flask import current_app
from models import User, UserInvestorMap, InvestorInfo, UnitMap, ManagerInfo
from bases.globals import db
from bases.exceptions import AuthError, VerifyError, LogicError


def get_user(user_id):
    return User.get_by_id(user_id)


def get_user_by_mobile(mobile):
    return User.filter_by_query(mobile=mobile).first()


def get_user_investors(user, manager_id):
    investors = db.session.query(
        UserInvestorMap.map_type,
        InvestorInfo,
        UnitMap.name,
    ).filter(
        UserInvestorMap.user_id == user.id,
        InvestorInfo.investor_id == UserInvestorMap.investor_id,
        UnitMap.investor_id == UserInvestorMap.investor_id,
        UnitMap.manager_id == manager_id,
        UnitMap.is_deleted == False,
    ).all()

    ret = []
    for i in investors:
        d = i[1].to_dict()
        d['map_type'] = i[0]
        d['map_name'] = i[2]
        d['manager_id'] = manager_id
        ret.append(d)
    return ret


def chose_investor(user, manager, investor_id=None):
    investors = get_user_investors(user, manager.manager_id)
    investor_ids = {i['investor_id']: i for i in investors}

    if len(investors) < 1:
        raise VerifyError('账户不存在！')

    if investor_id:
        if investor_id not in investor_ids:
            raise VerifyError('客户编码不存在！')
        return investor_ids[investor_id]

    if user.last_login_investor:
        if user.last_login_investor not in investor_ids:
            raise VerifyError('客户编码关系错误！')
        return investor_ids[user.last_login_investor]

    return investors[0]

