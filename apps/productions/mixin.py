
import pandas as pd
import datetime

from flask import request, g
from utils.helper import generate_sql_pagination, replace_nan
from utils.decorators import login_required
from bases.globals import db
from models import FOFInfo, FOFNav, FOFNavPublic


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


class ViewList(ViewObject):

    @login_required
    def get(self, fof_id):
        p = generate_sql_pagination()

        query = self.model.filter_by_query(
            fof_id=fof_id
        )
        data = p.paginate(query)
        return data


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


class ProMixin:
    nav_model = None

    def select_model(self, fof_id):
        obj = FOFInfo.filter_by_query(
            fof_id=fof_id,
            manager_id=g.token.manager_id,
        ).first()
        if obj:
            self.nav_model = FOFNav
            return obj
        else:
            self.nav_model = FOFNavPublic
            return FOFInfo.get_by_query(
                fof_id=fof_id,
                manager_id='1',
            )

    def calc_fof_ret(self, fof_id):
        start_date = None if not request.args.get('start_date') else \
            datetime.datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
        end_date = None if not request.args.get('end_date') else \
            datetime.datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')

        results = db.session.query(
            self.nav_model.datetime,
            self.nav_model.ret,
            self.nav_model.nav,
            self.nav_model.acc_net_value,
            self.nav_model.adjusted_nav,
        ).filter(
            self.nav_model.fof_id == fof_id,
        ).order_by(
            self.nav_model.datetime.asc()
        ).all()

        if len(results) < 1:
            return []

        df = pd.DataFrame([{
            'datetime': i[0],
            'acc_ret': i[1],
            'nav': i[2],
            'acc_net_value': i[3],
            'adjusted_nav': i[4],
        } for i in results])

        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')
        df['all_nav'] = df['adjusted_nav'] / df['adjusted_nav'][0]
        df['daily_ret'] = df['all_nav'] / df['all_nav'].shift(1) - 1

        if start_date:
            df = df[df.index >= start_date]

        if end_date:
            df = df[df.index <= end_date]

        return df
