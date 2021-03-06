
import datetime
import itertools

from collections import defaultdict
from sqlalchemy import func

from bases.globals import db
from models import FOFInfo, FOFInvestorPosition, FOFNotification, InfoDetail, InfoToProduction, NotificationActive, UnitMap
from utils.helper import parse_date_counts

from .constants import CONTENT_TYPE_TO_NOTIFICATION_TYPE


def get_fofs(manager_id):
    fofs = FOFInfo.filter_by_query(manager_id=manager_id).all()
    return {fof.fof_id: fof.fof_name for fof in fofs}


def get_productions(manager_id, model):
    fofs = get_fofs(manager_id)
    for item in model.filter_by_query(manager_id=manager_id).all():
        if item.fof_id not in fofs:
            continue
        yield item, {'fof_id': item.fof_id, 'fof_name': fofs[item.fof_id]}


def get_contents(manager_id):
    contents = InfoDetail.filter_by_query(manager_id=manager_id).filter(InfoDetail.info_type != 3).all()

    productions = defaultdict(list)
    for item, production in get_productions(manager_id, InfoToProduction):
        productions[item.info_id].append(production)

    content_ids = FOFNotification.get_manager_content_ids(manager_id)

    return [{
        'productions': productions[content.id],
        'notified': content.id in content_ids,
        **content.to_dict(),
    } for content in contents]


def get_customers(manager_id):
    units = UnitMap.filter_by_query(manager_id=manager_id).all()

    productions = defaultdict(list)
    for item, production in get_productions(manager_id, FOFInvestorPosition):
        productions[item.investor_id].append(production)

    investor_counts = FOFNotification.get_investor_counts(manager_id)

    return [{
        'productions': productions[unit.investor_id],
        'read_count': investor_counts.get(unit.investor_id, {}).get(True, 0),
        'unread_count': investor_counts.get(unit.investor_id, {}).get(False, 0),
        **unit.to_dict(),
    } for unit in units]


def save_notification(manager_id, investor_ids, contents):
    for investor_id, content in itertools.product(investor_ids, contents):
        FOFNotification(
            manager_id=manager_id,
            investor_id=investor_id,
            notification_type=CONTENT_TYPE_TO_NOTIFICATION_TYPE[content['content_type']],
            content_id=content['content_id'],
            content=content['content'],
        ).save(commit=False)
    db.session.commit()


def get_investor_counts(manager_id, start_time):
    date_counts = db.session.query(
        func.date(UnitMap.create_time),
        func.count(UnitMap.id),
    ).filter_by(
        manager_id=manager_id,
    ).filter(
        UnitMap.create_time > start_time,
    ).group_by(
        func.date(UnitMap.create_time),
    ).all()

    dates, counts = parse_date_counts(date_counts)
    return {
        'dates': dates,
        'counts': counts,
        'total': sum(counts),
    }


def get_notification_statistics(manager_id, days):
    start_time = datetime.datetime.now() - datetime.timedelta(days=days)
    start_date = start_time.date()

    notification_investor = get_investor_counts(manager_id, start_time)
    notification_active = NotificationActive.get_active_counts(manager_id, start_date)
    notification_count = FOFNotification.get_notification_counts(manager_id, start_time)
    notification_read_count = FOFNotification.get_notification_counts(manager_id, start_time, filter_read=True)

    return {
        'start_date': str(start_date),
        'notification_investor': notification_investor,
        'notification_active': notification_active,
        'notification_count': notification_count,
        'notification_read_count': notification_read_count,
    }

