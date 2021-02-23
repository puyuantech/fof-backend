from bases.globals import settings
from surfing.data.manager.manager_fof import FOFDataManager


def update_fof(fof_id=None):
    fof_dm = FOFDataManager()
    fof_dm.calc_fof_nav()

