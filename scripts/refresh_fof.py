from bases.globals import settings
from surfing.data.manager.manager_fof_lite import FOFDataManagerLite


def update_fof(fof_id, manager_id):
    fof_dm = FOFDataManagerLite()
    fof_dm.calc_fof_nav(fof_id=fof_id, manager_id=manager_id)


def update_public_fof(fof_id, manager_id):
    fof_dm = FOFDataManagerLite()
    fof_dm.calc_pure_fof_data(fof_id=fof_id, manager_id=manager_id)

