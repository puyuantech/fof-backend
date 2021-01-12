import uuid
import base64
import random

from bases.viewhandler import ApiViewHandler
from utils.decorators import params_required
from models import CaptchaCode, MobileCode
from surfing.data.manager.manager_fof import FOFDataManager


class ProductionAPI(ApiViewHandler):
    def get(self):
        df = FOFDataManager.get_fof_info()
        return df.to_dict(orient='r')

