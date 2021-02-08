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


class ViewAllMixin:
    model = None
    parse_func = None
    update_func = None

    @login_required
    def get(self, fof_id):
        p = generate_sql_pagination()

        query = self.model.filter_by_query(
            fof_id=fof_id
        )
        data = p.paginate(query)
        return data

    @login_required
    def put(self, fof_id):
        df = self.parse_func(fof_id)

        for d in df.to_dict(orient='records'):
            new = self.model(**replace_nan(d))
            db.session.add(new)
        db.session.commit()

    @login_required
    def post(self, fof_id):
        obj = self.model(
            fof_id=fof_id,
        )
        self.update_func(obj)

    @login_required
    def delete(self, fof_id):
        self.model.filter_by_query(fof_id=fof_id).delete()

