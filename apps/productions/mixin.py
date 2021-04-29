
import pandas as pd
import datetime

from flask import request, g
from utils.helper import generate_sql_pagination, replace_nan
from utils.decorators import login_required
from bases.globals import db
from models import FOFInfo, FOFNav, FOFNavPublic, FOFUnconfirmedNav


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
    def select_model(self, fof_id):
        obj = FOFInfo.filter_by_query(
            fof_id=fof_id,
            manager_id=g.token.manager_id,
        ).first()
        if obj:
            return obj
        else:
            return FOFInfo.get_by_query(
                fof_id=fof_id,
                manager_id='1',
            )

    def calc_fof_ret(self, fof_id, unconfirmed=False):
        start_date = None if not request.args.get('start_date') else \
            datetime.datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
        end_date = None if not request.args.get('end_date') else \
            datetime.datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')

        df_pub = self.get_public_nav(fof_id)
        df_pri = self.get_private_nav(fof_id)

        df = df_pub.copy()
        if len(df_pri) > 0:
            for i in df_pri.index:
                df = df.append(df_pri.loc[i, :], ignore_index=True)

        df['is_unconfirmed'] = False

        # 获取未确认净值
        if unconfirmed:
            df_unc = self.get_unconfirmed_nav(fof_id)
            for i in df_unc.index:
                df = df.append(df_unc.loc[i, :], ignore_index=True)

        if len(df) < 1:
            return []

        df = df.drop_duplicates(subset=['datetime'], keep='last')
        df = df.set_index('datetime')
        df['all_nav'] = df['adjusted_nav'] / df['adjusted_nav'][0]
        df['daily_ret'] = df['all_nav'] / df['all_nav'].shift(1) - 1
        df = df.sort_values('datetime')

        if start_date:
            df = df[df.index >= start_date]

        if end_date:
            df = df[df.index <= end_date]

        return df

    def get_public_nav(self, fof_id):

        results = db.session.query(
            FOFNavPublic.datetime,
            FOFNavPublic.ret,
            FOFNavPublic.nav,
            FOFNavPublic.acc_net_value,
            FOFNavPublic.adjusted_nav,
        ).filter(
            FOFNavPublic.fof_id == fof_id,
        ).order_by(
            FOFNavPublic.datetime.asc()
        ).all()

        if len(results) < 1:
            return pd.DataFrame([], columns=[
                'datetime',
                'acc_ret',
                'acc_net_value',
                'nav',
                'adjusted_nav',
            ])

        df = pd.DataFrame([{
            'datetime': i[0],
            'acc_ret': i[1],
            'nav': i[2],
            'acc_net_value': i[3],
            'adjusted_nav': i[4],
        } for i in results])

        df['datetime'] = pd.to_datetime(df['datetime'])
        return df

    def get_private_nav(self, fof_id):
        results = db.session.query(
            FOFNav.datetime,
            FOFNav.ret,
            FOFNav.nav,
            FOFNav.acc_net_value,
            FOFNav.adjusted_nav,
        ).filter(
            FOFNav.fof_id == fof_id,
            FOFNav.manager_id == g.token.manager_id,
        ).order_by(
            FOFNav.datetime.asc()
        ).all()

        if len(results) < 1:
            return pd.DataFrame([])

        df = pd.DataFrame([{
            'datetime': i[0],
            'acc_ret': i[1],
            'nav': i[2],
            'acc_net_value': i[3],
            'adjusted_nav': i[4],
        } for i in results])

        df['datetime'] = pd.to_datetime(df['datetime'])
        return df

    def get_unconfirmed_nav(self, fof_id):
        results = db.session.query(
            FOFUnconfirmedNav.datetime,
            FOFUnconfirmedNav.nav,
            FOFUnconfirmedNav.acc_net_value,
        ).filter(
            FOFUnconfirmedNav.fof_id == fof_id,
            FOFUnconfirmedNav.manager_id == g.token.manager_id,
            FOFUnconfirmedNav.is_deleted == False,
        ).order_by(
            FOFUnconfirmedNav.datetime.asc()
        ).all()

        if len(results) < 1:
            return pd.DataFrame([])

        df = pd.DataFrame([{
            'datetime': i[0],
            'nav': i[1],
            'acc_net_value': i[2],
        } for i in results])

        df['is_unconfirmed'] = True
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df
