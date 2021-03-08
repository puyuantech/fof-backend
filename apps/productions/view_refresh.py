import os
from bases.viewhandler import ApiViewHandler
from bases.globals import settings
from bases.exceptions import VerifyError
from utils.decorators import admin_login_required
from utils.process import subprocess_popen
from models import FOFInfo
from bases.constants import StuffEnum


class ProductionRefresh(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def get(self, fof_id):

        obj = FOFInfo.filter_by_query(
            fof_id=fof_id
        ).one_or_none()
        if not obj:
            raise VerifyError('不存在！')

        obj.is_calculating = True
        obj.save()

        log_file = os.path.join(
            settings['LOG_PATH'],
            '{}.sub.log'.format(fof_id),
        )
        subprocess_popen(['python', 'manager.py', 'update_fof', '--id={}'.format(fof_id)], log_file)


class ProductionPublicRefresh(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def get(self, fof_id):

        obj = FOFInfo.filter_by_query(
            fof_id=fof_id
        ).one_or_none()
        if not obj:
            raise VerifyError('不存在！')

        obj.is_calculating = True
        obj.save()

        log_file = os.path.join(
            settings['LOG_PATH'],
            '{}.sub.log'.format(fof_id),
        )
        subprocess_popen(['python', 'manager.py', 'pub_fof', '--id={}'.format(fof_id)], log_file)

