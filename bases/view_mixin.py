import pandas as pd
from utils.helper import generate_sql_pagination, replace_nan
from utils.decorators import login_required
from bases.globals import db


class ViewDetailMixin:
    model = None
    update_func = None

    @login_required
    def put(self, _id):
        obj = self.model.get_by_id(_id)
        self.update_func(obj)

    @login_required
    def delete(self, _id):
        obj = self.model.get_by_id(_id)
        obj.delete()


class ViewObject:
    model = None
    parse_func = None
    update_func = None

    def get_objects(self):
        return self.model.filter_by_query()


class ViewList(ViewObject):

    @login_required
    def get(self):
        p = generate_sql_pagination()

        query = self.get_objects()
        data = p.paginate(query)
        return data

