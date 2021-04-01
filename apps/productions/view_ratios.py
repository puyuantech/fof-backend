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
from models import FOFNavPublic, FOFInfo, FOFNav, Management, ManagementFund
from surfing.util.calculator import Calculator
from .mixin import ProMixin


class ProInfoAPI(ApiViewHandler, ProMixin):

    @login_required
    def get(self, fof_id):
        """详情"""
        obj = self.select_model(fof_id)
        if not obj:
            return {}

        data = obj.to_dict()
        fund = ManagementFund.filter_by_query(
            fund_no=fof_id,
        ).first()
        if fund:
            data.update({
                'establish_date': fund.establish_date,
                'filing_date': fund.filing_date,
                'filing_stage': fund.filing_stage,
                'fund_type': fund.fund_type,
                'currency_type': fund.currency_type,
                'management_type': fund.management_type,
                'custodian_name': fund.custodian_name,
                'fund_status': fund.fund_status,
                'special_reminder': fund.special_reminder,
                'update_date': fund.update_date,
            })
        return data


class ProManagementAPI(ApiViewHandler, ProMixin):

    @login_required
    def get(self, fof_id):
        """详情"""
        fund = ManagementFund.filter_by_query(
            fund_no=fof_id,
        ).first()
        if not fund:
            return {}

        management_ids = fund.manager_ids if fund.manager_ids else []
        if not management_ids:
            return {}

        m = Management.filter_by_query(
            manager_id=management_ids[0],
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
        df['ret'] = df['adjusted_nav'] / df['adjusted_nav'].shift(1) - 1
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

