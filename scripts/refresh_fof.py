
import traceback
from bases.globals import settings
from models import FOFCalcStatus
from surfing.data.manager.manager_fof_lite import FOFDataManagerLite


def update_fof(fof_id, manager_id):
    obj = FOFCalcStatus.create(
        fof_id=fof_id,
        manager_id=manager_id,
        status=FOFCalcStatus.StatusEnum.PENDING,
    )
    try:
        fof_dm = FOFDataManagerLite()
        fof_dm.calc_fof_nav(fof_id=fof_id, manager_id=manager_id)
    except Exception as e:
        obj.status = FOFCalcStatus.StatusEnum.FAILED
        obj.failed_reason = traceback.format_exc()
        obj.save()
    else:
        obj.status = FOFCalcStatus.StatusEnum.SUCCESS
        obj.save()


def update_public_fof(fof_id, manager_id):
    obj = FOFCalcStatus.create(
        fof_id=fof_id,
        manager_id=manager_id,
        status=FOFCalcStatus.StatusEnum.PENDING,
    )
    try:
        fof_dm = FOFDataManagerLite()
        fof_dm.calc_pure_fof_data(fof_id=fof_id, manager_id=manager_id)
    except Exception as e:
        obj.status = FOFCalcStatus.StatusEnum.FAILED
        obj.failed_reason = traceback.format_exc()
        obj.save()
    else:
        obj.status = FOFCalcStatus.StatusEnum.SUCCESS
        obj.save()
