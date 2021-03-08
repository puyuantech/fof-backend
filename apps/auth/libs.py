import datetime
from models import User, UserInvestorMap, InvestorInfo, UnitMap
from bases.globals import db
from bases.exceptions import AuthError, VerifyError, LogicError


def get_user(user_id):
    return User.get_by_id(user_id)


def get_user_by_mobile(mobile):
    return User.filter_by_query(mobile=mobile).first()


def get_user_investors(user):
    investors = db.session.query(
        UserInvestorMap.map_type,
        InvestorInfo,
    ).filter(
        UserInvestorMap.user_id == user.id,
        InvestorInfo.investor_id == UserInvestorMap.investor_id,
    ).all()

    ret = []
    for i in investors:
        d = i[1].to_dict()
        d['map_type'] = i[0]
        ret.append(d)

    return ret


def generate_investor_id(manager_id, user_id):
    return manager_id.lower() + str(hex(user_id))[2:]


def create_main_investor(user, manager, mobile):
    investor_id = generate_investor_id(manager.manager_id, user.id)
    investor = InvestorInfo(
        investor_id=investor_id,
        mobile_phone=mobile,
    )
    investor_map = UserInvestorMap(
        user_id=user.id,
        investor_id=investor_id,
    )
    manager_investor_map = UnitMap(
        manager_id=manager.manager_id,
    )
    db.session.add(investor)


def chose_investor(user, investor_id):
    pass



