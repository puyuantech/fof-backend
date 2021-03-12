
import traceback

from flask import current_app
from pydantic import ValidationError

from bases.exceptions import NotFoundError
from bases.globals import db
from extensions.manager.spider import ManagementSpider
from extensions.manager.validator import ManagementBaseValidation, ManagementInfoValidation, ManageFundValidation
from models import Management, ManagementFund


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
            current_app.logger.info(f'[update_manager_list] done! (manager_count){manager_count}')
        except Exception:
            current_app.logger.error(f'[update_manager_list] failed! (manager_count){manager_count} (err_msg){traceback.format_exc()}')
            return False

    current_app.logger.info(f'[update_manager_list] all done! (manager_count){manager_count}')
    return True


def update_funds(fund_ids: list):
    for fund_id in fund_ids:
        ManagementFund(fund_id=fund_id).save(commit=False)
    db.session.commit()


def update_manager_info(start=0):
    managers = Management.filter_by_query().all()
    funds = db.session.query(ManagementFund.fund_id).filter_by(is_deleted=False).all()
    funds = {fund_id for fund_id, in funds}

    manager_count = 0
    for manager in managers:
        manager_count += 1
        if manager_count <= start:
            continue

        try:
            manager_info = ManagementSpider.get_manager_info(manager.manager_id)
            manager_info_validation = ManagementInfoValidation.get_manager(manager_info)

        except NotFoundError:
            manager.logic_delete()

        except ValidationError as e:
            current_app.logger.error(f'[update_manager_info] failed! (manager_id){manager.manager_id} (manager_info){manager_info} (err_msg){e}')
            return False

        else:
            if manager.update_date != manager_info_validation.update_date:
                manager.update(**manager_info_validation.dict())

            # 产品信息
            fund_ids = set(manager_info_validation.fund_ids).difference(funds)
            if fund_ids:
                update_funds(fund_ids)
                funds.update(fund_ids)

        if manager_count % 100 == 0:
            current_app.logger.info(f'[update_manager_info] done! (manager_count){manager_count}')

    current_app.logger.info(f'[update_manager_info] all done! (manager_count){manager_count}')
    return True


def update_fund_info(start=0):
    funds = ManagementFund.filter_by_query().all()

    fund_count = 0
    for fund in funds:
        fund_count += 1
        if fund_count <= start:
            continue

        try:
            fund_info = ManagementSpider.get_fund_info(fund.fund_id)
            fund_info_validation = ManageFundValidation.get_fund(fund_info)

        except NotFoundError:
            fund.logic_delete()

        except ValidationError as e:
            current_app.logger.error(f'[update_fund_info] failed! (fund_id){fund.fund_id} (fund_info){fund_info} (err_msg){e}')
            return False

        else:
            if fund.update_date != fund_info_validation.update_date:
                fund.update(**fund_info_validation.dict())

        if fund_count % 100 == 0:
            current_app.logger.info(f'[update_fund_info] done! (fund_count){fund_count}')

    current_app.logger.info(f'[update_fund_info] all done! (fund_count){fund_count}')
    return True


def update_managements(manager_list=True, manager_info=True, fund_info=True, start=0):
    if manager_list and not update_manager_list(start):
        return

    if manager_info and not update_manager_info(start):
        return

    if fund_info and not update_fund_info(start):
        return

