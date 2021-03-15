
import datetime
import pathlib
import traceback

from flask import current_app
from pydantic import ValidationError

from bases.exceptions import NotFoundError
from bases.globals import db
from extensions.manager.spider import ManagementSpider
from extensions.manager.validator import (ManagementBaseValidation, ManagementInfoValidation,
                                          ManageFundValidation, ManagementSeniorValidation,
                                          ManagementRelatedPartyValidation, ManagementInvestorValidation)
from models import Management, ManagementFund, ManagementSenior, ManagementRelatedParty, ManagementInvestor


def now_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def log_message(path, message):
    with open(path, 'a') as f:
        f.write(message + '\n')


def update_manager_list(start=0):
    managers = Management.filter_by_query().all()
    managers = {manager.manager_id: manager for manager in managers}

    manager_count = 0
    for manager_list in ManagementSpider.get_manager_list():
        manager_count += len(manager_list)
        if manager_count <= start:
            continue

        for manager in manager_list:
            manager_validation = ManagementBaseValidation.get_manager(manager)
            if manager_validation.manager_id not in managers:
                Management(**manager_validation.dict()).save(commit=False)
                continue

            try:
                if manager_validation == ManagementBaseValidation(**managers[manager_validation.manager_id].to_dict()):
                    continue
            except ValidationError:
                pass
            managers[manager_validation.manager_id].update(commit=False, **manager_validation.dict())

        try:
            db.session.commit()
            current_app.logger.info(f'[update_manager_list][{now_time()}] done! (manager_count){manager_count}')
        except Exception:
            current_app.logger.error(f'[update_manager_list][{now_time()}] failed! (manager_count){manager_count} (err_msg){traceback.format_exc()}')
            return False

    current_app.logger.info(f'[update_manager_list][{now_time()}] all done! (manager_count){manager_count}')
    return True


def update_funds(fund_ids: list):
    for fund_id in fund_ids:
        ManagementFund(fund_id=fund_id).save(commit=False)
    db.session.commit()


def update_seniors(manager_id, senior_infos: list):
    for senior_info in senior_infos:
        senior_validation = ManagementSeniorValidation.get_senior(senior_info)
        ManagementSenior(manager_id=manager_id, **senior_validation.dict()).save(commit=False)
    db.session.commit()


def update_related_parties(manager_id, related_parties: list):
    for related_party in related_parties:
        related_party_validation = ManagementRelatedPartyValidation.get_related_party(related_party)
        ManagementRelatedParty(manager_id=manager_id, **related_party_validation.dict()).save(commit=False)
    db.session.commit()


def update_investors(manager_id, investors: list):
    for investor in investors:
        investor_validation = ManagementInvestorValidation.get_investor(investor)
        ManagementInvestor(manager_id=manager_id, **investor_validation.dict()).save(commit=False)
    db.session.commit()


def update_manager_info(start, path):
    error_exceptions_path = path / 'error_exceptions.log'
    error_managers_path = path / 'error_managers.log'

    managers = Management.filter_by_query().all()
    funds = ManagementFund.get_fund_ids()
    senior_managers = ManagementSenior.get_manager_ids()
    related_party_managers = ManagementRelatedParty.get_manager_ids()
    investor_managers = ManagementInvestor.get_manager_ids()

    manager_count = start
    for manager in managers[start:]:
        manager_count += 1

        try:
            manager_info = ManagementSpider.get_manager_info(manager.manager_id)
            manager_info_validation = ManagementInfoValidation.get_manager(manager_info)

            if manager.update_date != manager_info_validation.update_date:
                manager.update(**manager_info_validation.dict())

            # 产品信息
            fund_ids = set(manager_info_validation.fund_ids).difference(funds)
            if fund_ids:
                update_funds(fund_ids)
                funds.update(fund_ids)

            # 高管信息
            if manager.manager_id not in senior_managers and manager_info['高管信息']:
                update_seniors(manager.manager_id, manager_info['高管信息'])

            # 关联方信息
            if manager_info['关联方信息'] and manager.manager_id not in related_party_managers:
                update_related_parties(manager.manager_id, manager_info['关联方信息'])

            # 出资人信息
            if manager.manager_id not in investor_managers and manager_info['出资人信息']:
                update_investors(manager.manager_id, manager_info['出资人信息'])

        except NotFoundError:
            manager.logic_delete()

        except ValidationError:
            err_msg = f'[update_manager_info][{now_time()}] failed! (manager_id){manager.manager_id} (manager_info){manager_info} (err_msg){traceback.format_exc()}'
            current_app.logger.error(err_msg)
            log_message(error_exceptions_path, err_msg)
            log_message(error_managers_path, str(manager.manager_id))

        except Exception:
            err_msg = f'[update_manager_info][{now_time()}] failed! (manager_id){manager.manager_id} (err_msg){traceback.format_exc()}'
            current_app.logger.error(err_msg)
            log_message(error_exceptions_path, err_msg)
            log_message(error_managers_path, str(manager.manager_id))

        if manager_count % 100 == 0:
            current_app.logger.info(f'[update_manager_info][{now_time()}] done! (manager_count){manager_count}')

    current_app.logger.info(f'[update_manager_info][{now_time()}] all done! (manager_count){manager_count}')
    return True


def update_fund_info(start, path):
    error_exceptions_path = path / 'error_exceptions.log'
    error_funds_path = path / 'error_funds.log'

    funds = ManagementFund.filter_by_query().all()

    fund_count = start
    for fund in funds[start:]:
        fund_count += 1

        try:
            fund_info = ManagementSpider.get_fund_info(fund.fund_id)
            fund_info_validation = ManageFundValidation.get_fund(fund_info)

            if fund.update_date != fund_info_validation.update_date:
                fund.update(**fund_info_validation.dict())

        except NotFoundError:
            fund.logic_delete()

        except ValidationError:
            err_msg = f'[update_fund_info][{now_time()}] failed! (fund_id){fund.fund_id} (fund_info){fund_info} (err_msg){traceback.format_exc()}'
            current_app.logger.error(err_msg)
            log_message(error_exceptions_path, err_msg)
            log_message(error_funds_path, str(fund.fund_id))

        except Exception:
            err_msg = f'[update_fund_info][{now_time()}] failed! (fund_id){fund.fund_id} (err_msg){traceback.format_exc()}'
            current_app.logger.error(err_msg)
            log_message(error_exceptions_path, err_msg)
            log_message(error_funds_path, str(fund.fund_id))

        if fund_count % 100 == 0:
            current_app.logger.info(f'[update_fund_info][{now_time()}] done! (fund_count){fund_count}')

    current_app.logger.info(f'[update_fund_info][{now_time()}] all done! (fund_count){fund_count}')
    return True


def update_managements(manager_list=True, manager_info=True, fund_info=True, start=0, path=None):
    if path is not None:
        path = pathlib.Path(path)
        if not path.is_dir():
            path = None
    if path is None:
        path = pathlib.Path(__file__).parent.absolute()

    if manager_list and not update_manager_list(start):
        return

    if manager_info and not update_manager_info(start, path):
        return

    if fund_info and not update_fund_info(start, path):
        return

