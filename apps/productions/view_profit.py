import pandas as pd
import empyrical as ep
import datetime
from flask import request
from bases.viewhandler import ApiViewHandler
from bases.globals import db
from bases.exceptions import VerifyError
from utils.decorators import login_required
from utils.helper import replace_nan
from utils.queries import SurfingQuery
from utils.ratios import yearly_return
from models import FOFNavPublic
from surfing.util.calculator import Calculator


def calc_fof_ret(fof_id):
    start_date = None if not request.args.get('start_date') else \
        datetime.datetime.strptime(request.args.get('start_date'), '%Y-%m-%d').date()
    end_date = None if not request.args.get('end_date') else \
        datetime.datetime.strptime(request.args.get('end_date'), '%Y-%m-%d').date()

    results = db.session.query(
        FOFNavPublic.datetime,
        FOFNavPublic.ret,
        FOFNavPublic.nav,
        FOFNavPublic.acc_net_value,
    ).filter(
        FOFNavPublic.fof_id == fof_id,
    ).order_by(
        FOFNavPublic.datetime.asc()
    ).all()

    df = pd.DataFrame([{
        'datetime': i[0],
        'acc_ret': i[1],
        'nav': i[2],
        'acc_net_value': i[3],
    } for i in results])

    df['temp'] = df['acc_ret'] + 1
    df['daily_ret'] = df['temp'] / df['temp'].shift(1) - 1

    if start_date:
        df = df[df['datetime'] >= start_date]

    if end_date:
        df = df[df['datetime'] <= end_date]

    return df


def calc_index_ret(index_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    df = SurfingQuery.get_index_point(
        index_id,
        start_date,
        end_date,
        ('ret',),
    )
    df = df.set_index('datetime')
    return df


class ProductionRet(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        df = calc_fof_ret(fof_id)
        if len(df) < 1:
            return {}

        data = {
            'acc_net_value': df['temp'],
            'dates': df['datetime'],
        }
        return replace_nan(data)


class ProductionMonthlyRet(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        df = calc_fof_ret(fof_id)
        if len(df) < 1:
            return {}

        df = df.set_index('datetime')
        returns = df['daily_ret']
        ret = ep.aggregate_returns(returns, 'monthly')
        ret = pd.DataFrame(ret)
        ret.index = ['{}-{}'.format(index[0], index[1]) for index in ret.index]

        data = {
            'ret': ret['daily_ret'].to_list(),
            'month': ret.index,
            'yearly': yearly_return(returns),
        }
        return replace_nan(data)


class ProductionRatio(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        """
        计算 fof 产品的区间指标
        :param fof_id:
        :return: {
            单位净值
            累计净值
            期间收益
            年初至期末
            最大回撤
            夏普比率
        }
        """
        df = calc_fof_ret(fof_id)
        if len(df) < 1:
            return {}
        ratios = Calculator.get_stat_result_from_df(df, 'datetime', 'temp')
        # year_to_now = df.iloc[0]['temp'] / \
        #     df[df['datetime'] < datetime.date(df.iloc[0]['datetime'].year, 1, 1)].iloc[0]['temp'] - 1 \
        #     if len(df[df['datetime'] < datetime.date(df.iloc[0]['datetime'].year, 1, 1)]) > 0 else None
        # ret = df.iloc[0]['temp'] / df.iloc[-1]['temp'] - 1 if df.iloc[-1]['temp'] else None

        data = {
            'acc_net_value': df.iloc[0]['acc_net_value'],
            'nav': df.iloc[0]['nav'],
            'datetime': df.iloc[0]['datetime'],
            'mdd': ratios.mdd,
            'sharpe': ratios.sharpe,
            'ret': df.iloc[-1]['temp'] / df.iloc[0]['temp'] - 1 if df.iloc[0]['temp'] else None,
            # 'year_to_now': year_to_now if year_to_now else ret,
        }
        return replace_nan(data)


class ProductionWinRate(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        index_id = request.args.get('index_id')
        if not index_id:
            raise VerifyError('No index id')

        df = calc_fof_ret(fof_id)
        if len(df) < 1:
            return {}

        index_df = calc_index_ret(index_id=index_id)
        if len(index_df) < 1:
            return {}

        df = df.set_index('datetime')
        df = df.reindex(index_df.index)
        index_df['minus'] = df['daily_ret'] - index_df['ret']

        rate = len(index_df[index_df['minus'] >= 0]) / len(index_df)
        data = {
            'rate': rate,
        }
        return replace_nan(data)
