import uuid
import base64
import random

from bases.viewhandler import ApiViewHandler
from bases.paginations import SQLPagination
from models import FOFInfo
from utils.decorators import params_required
from utils.helper import generate_sql_pagination


class ProductionsAPI(ApiViewHandler):
    def get(self):
        p = generate_sql_pagination()
        query = FOFInfo.filter_by_query()
        data = p.paginate(query)
        return data

    def post(self):
        pass


class ProductionAPI(ApiViewHandler):
    def get(self, _id):
        obj = FOFInfo.get_by_query(fof_id=_id)
        return obj.to_dict()

    def post(self, _id):
        pass


class ProductionDetail(ApiViewHandler):
    def get(self, _id):
        p = generate_sql_pagination()
        query = FOFInfo.filter_by_query()
        data = p.paginate(query)
        return data

    def post(self, _id):
        pass
