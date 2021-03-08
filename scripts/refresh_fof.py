from bases.globals import settings
from surfing.data.manager.manager_fof import FOFDataManager


def update_fof(fof_id):
    fof_dm = FOFDataManager()
    fof_dm.calc_fof_nav(fof_id=fof_id)


def update_public_fof(fof_id):
    fof_dm = FOFDataManager()
    fof_dm.calc_pure_fof_data(fof_id=fof_id)

