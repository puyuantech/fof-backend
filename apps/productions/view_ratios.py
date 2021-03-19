import pandas as pd
import datetime
import json
from flask import request, g
from bases.viewhandler import ApiViewHandler
from bases.globals import db
from bases.exceptions import VerifyError
from utils.decorators import login_required
from utils.helper import replace_nan
from utils.ratios import draw_down_underwater, monthly_return, yearly_return
from utils.helper import select_periods
from models import FOFNavPublic, FOFInfo, FOFNav, Management
from surfing.util.calculator import Calculator


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


class ProInfoAPI(ApiViewHandler, ProMixin):

    @login_required
    def get(self, fof_id):
        """详情"""
        obj = self.select_model(fof_id)
        if not obj:
            return {}
        return obj.to_dict()


class ProManagementAPI(ApiViewHandler, ProMixin):

    @login_required
    def get(self, fof_id):
        """详情"""
        obj = self.select_model(fof_id)
        if not obj:
            return {}

        management_ids = json.loads(obj.management_ids) if obj.management_ids else []
        if not management_ids:
            return {}

        m = Management.filter_by_query(
            manager_id=management_ids,
        ).first()
        if not m:
            return {}

        return m.to_dict()


class ProNavAPI(ApiViewHandler, ProMixin):

    @login_required
    def get(self, fof_id):
        """净值"""
        # trading_days = cache_trading_days()
        self.select_model(fof_id)
        period = select_periods()

        df = self.calc_fof_ret(fof_id)
        if len(df) < 1:
            return {}

        if period:
            df = df.resample(period).last().fillna(method='ffill')

        df = df.reset_index()
        df = df[[
            'datetime',
            'adjusted_nav',
            'nav',
            'acc_net_value',
        ]]
        df['ret'] = df['adjusted_nav'] / df['adjusted_nav'][0] - 1
        data = df.to_dict(orient='list')
        return replace_nan(data)


class ProMonthlyRetAPI(ApiViewHandler, ProMixin):

    @login_required
    def get(self, fof_id):
        self.select_model(fof_id)
        """月度收益"""
        df = self.calc_fof_ret(fof_id)
        if len(df) < 1:
            return {}

        returns = df['daily_ret']
        data = {
            'monthly': monthly_return(returns),
        }
        return replace_nan(data)


class ProPeriodRetAPI(ApiViewHandler, ProMixin):

    @login_required
    def get(self, fof_id):
        """区间收益"""
        self.select_model(fof_id)
        df = self.calc_fof_ret(fof_id)
        if len(df) < 1:
            return {}

        data = Calculator.get_recent_ret(df.index, df['all_nav']).__dict__
        return replace_nan(data)


class ProRatioAPI(ApiViewHandler, ProMixin):

    @login_required
    def get(self, fof_id):
        """区间指标"""
        self.select_model(fof_id)
        df = self.calc_fof_ret(fof_id)
        if len(df) < 1:
            return {}

        period = select_periods()
        if period:
            arr = df['adjusted_nav'].resample(period).last().fillna(method='ffill')
        else:
            arr = df['adjusted_nav']

        data = Calculator.get_stat_result(arr.index, arr.values).__dict__
        benchmark = request.args.get('benchmark')
        if benchmark:
            return

        return replace_nan(data)


class ProRollingProfitAPI(ApiViewHandler, ProMixin):

    # 月 -> 周
    period_rule = {
        1: 4,
        3: 13,
        6: 26,
        12: 52,
        24: 104,
        36: 156,
    }

    @login_required
    def get(self, fof_id):
        """滚动收益"""
        self.select_model(fof_id)
        period = select_periods()
        period_size = int(request.args.get('period_size', 6))

        df = self.calc_fof_ret(fof_id)
        if len(df) < 1:
            return {}

        period = period if period else 'W'
        period_size = period_size if period == 'M' else period_size * self.period_rule[period_size]
        arr = df['adjusted_nav'].resample(period).last().fillna(method='ffill')
        print(arr)
        ret = arr.pct_change(periods=period_size)
        ret = ret.dropna()

        data = {
            'values': ret.values,
            'dates': ret.index,
        }
        return replace_nan(data)


class ProDrawDownWaterAPI(ApiViewHandler, ProMixin):

    @login_required
    def get(self, fof_id):
        self.select_model(fof_id)
        df = self.calc_fof_ret(fof_id)
        if len(df) < 1:
            return {}
        period = select_periods()
        if period:
            arr = df['adjusted_nav'].resample(period).apply(lambda x: x[-1] if len(x) > 0 else None).fillna(method='ffill')
        else:
            arr = df['adjusted_nav']

        dff = draw_down_underwater(arr)

        data = {
            'values': dff.values,
            'dates': dff.index,
        }

        return replace_nan(data)

