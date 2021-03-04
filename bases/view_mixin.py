import pandas as pd
from flask import request
from utils.helper import generate_sql_pagination, replace_nan
from utils.decorators import login_required
from bases.globals import db


class ViewObject:
    model = None
    parse_func = None
    update_columns = []

    def get_objects(self):
        return self.model.filter_by_query()


class ViewDetailGet(ViewObject):

    @login_required
    def get(self, _id):
        obj = self.model.get_by_id(_id)
        return obj.to_dict()


class ViewDetailUpdate(ViewObject):

    @login_required
    def put(self, _id):
        obj = self.model.get_by_id(_id)

        for i in self.update_columns:
            if request.json.get(i) is not None:
                obj.update(commit=False, **{i: request.json.get(i)})
        obj.save()
        return


class ViewDetailDelete(ViewObject):

    @login_required
    def delete(self, _id):
        obj = self.model.get_by_id(_id)
        obj.delete()


class ViewList(ViewObject):

    @login_required
    def get(self):
        p = generate_sql_pagination()

        query = self.get_objects()
        data = p.paginate(query)
        return data


class ViewCreate(ViewObject):

    @login_required
    def put(self):
        p = generate_sql_pagination()

        query = self.get_objects()
        data = p.paginate(query)
        return data
