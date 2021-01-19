
from typing import List, Optional, Tuple, Union
from collections import defaultdict
import re
import datetime
import json
import io

import numpy as np
import pandas as pd

from ...util.singleton import Singleton
from ...util.wechat_bot import WechatBot
from ...constant import FundStatus, HoldingAssetType
from ..api.basic import BasicDataApi
from ..api.derived import DerivedDataApi
from ..view.basic_models import FOFManually, HedgeFundNAV
from ..view.derived_models import FOFNav, FOFPosition
from ..wrapper.mysql import BasicDatabaseConnector, DerivedDatabaseConnector


# def IncentiveFeeMode(enum.IntEnum):
#     ASSET_HW = 1  # 基金资产高水位方法
#     ASSET_HW_WITH_EXTRA = 2  # 基金资产高水位方法
#     SINGLE_CUSTOM_HW = 3  # 基金资产高水位）赎回时补充计提法
#     SINGLE_CUSTOM_HW_FIXED_WITH_EXTRA = 4  # （单客户高水位）固定时点扣减份额和赎回时补充计提法
#     SINGLE_CUSTOM_HW_DIVIDEND_WITH_EXTRA = 5  # （单客户高水位）分红时计提和赎回时补充计提法
#     SINGLE_CUSTOM_HW_OPEN_DAY = 6   # （单客户高水位）单客户开放日扣减净值计提法


class FOFDataManager(metaclass=Singleton):

    # 从EXCEL读取数据的路径，一般用不到
    _FILE_PATH = './nav_data/FOF运营计算逻辑.xlsx'

    # TODO: 暂时只支持一个FOF
    _FOF_ID = 'SLW695'

    _FEES_FLAG: List[int] = [1, 1, 1, 1, -1, -1, -1]
    _DAYS_PER_YEAR_FOR_INTEREST = 360

    def __init__(self):
        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.float_format', lambda x: '%.4f' % x)
        self._start_date: Optional[str] = None
        self._end_date: Optional[str] = None
        self._date_list: Optional[np.ndarray] = None
        self._fof_scale: Optional[pd.DataFrame] = None
        self._hedge_pos: Optional[pd.DataFrame] = None
        self._hedge_nav: Optional[pd.DataFrame] = None
        self._fund_pos: Optional[pd.DataFrame] = None
        self._manually: Optional[pd.DataFrame] = None
        self._fof_nav: Optional[pd.DataFrame] = None
        self._fof_position: Optional[pd.DataFrame] = None

        self._wechat_bot = WechatBot()

    def _get_days_this_year_for_fee(self, the_date: datetime.date) -> int:
        '''计算今年一共有多少天'''
        return pd.Timestamp(year=the_date.year, month=12, day=31).dayofyear

    @staticmethod
    def _do_calc_v_net_value(nav: Union[pd.Series, pd.DataFrame, float], init_water_line: pd.Series, incentive_fee_ratio: Union[pd.Series, float], decimals: Union[pd.Series, float]) -> pd.Series:
        # 盈利
        excess_ret = nav - init_water_line
        # 盈 或 亏
        earn_con = (excess_ret > 0).astype('int')
        # 费
        pay_mng_fee = excess_ret * earn_con * incentive_fee_ratio
        # 净值
        nav -= pay_mng_fee.round(decimals)
        nav = nav.round(decimals)
        return nav

    @staticmethod
    def _calc_virtual_net_value():
        '''计算虚拟净值'''
        fund_info = FOFDataManager.get_hedge_fund_info()
        # TODO: 目前只支持高水位法计算
        fund_info = fund_info.loc[fund_info.incentive_fee_mode == '高水位法']
        fund_info = fund_info.set_index('fund_id')

        df = FOFDataManager.get_hedge_fund_nav()
        df = df[df.fund_id.isin(fund_info.index.array)]
        df = df.sort_values(by=['fund_id', 'datetime', 'insert_time']).drop_duplicates(subset=['fund_id', 'datetime'], keep='last')

        asset_allocation = FOFDataManager.get_fof_asset_allocation()
        asset_allocation = asset_allocation[asset_allocation.status == FundStatus.INSENTIVE_DONE]

        trading_day_list = BasicDataApi().get_trading_day_list(start_date=df.datetime.sort_values().array[0], end_date=datetime.datetime.now().date())
        temp = df.pivot(index='datetime', columns='fund_id').reindex(trading_day_list.datetime).ffill()
        nav, _ = temp['net_asset_value'], temp['v_net_value']
        init_water_line = fund_info.water_line.to_frame('init_water_line')
        init_water_line['datetime'] = nav.index.array[0]
        init_water_line = init_water_line.reset_index().pivot(index='datetime', columns='fund_id', values='init_water_line').reindex(index=nav.index)
        for row in asset_allocation.itertuples(index=False):
            init_water_line.loc[row.datetime, row.fund_id] = nav.loc[nav.index < row.datetime].iloc[-2, :][row.fund_id]
        init_water_line = init_water_line.ffill()

        # print(f'do not support the incentive fee mode: {self._INCENTIVE_FEE_MODE}')
        return FOFDataManager._do_calc_v_net_value(nav, init_water_line, fund_info.incentive_fee_ratio, fund_info.v_nav_decimals)

    def init(self):
        # 获取fof基本信息
        fof_info: Optional[pd.DataFrame] = FOFDataManager.get_fof_info([FOFDataManager._FOF_ID])
        assert fof_info is not None, f'get fof info for {FOFDataManager._FOF_ID} failed'

        self._MANAGEMENT_FEE_PER_YEAR = fof_info.management_fee
        self._CUSTODIAN_FEE_PER_YEAR = fof_info.custodian_fee
        self._ADMIN_SERVICE_FEE_PER_YEAR = fof_info.administrative_fee
        self._DEPOSIT_INTEREST_PER_YEAR = fof_info.current_deposit_rate
        self._SUBSCRIPTION_FEE = fof_info.subscription_fee
        self._ESTABLISHED_DATE = fof_info.established_date
        self._INCENTIVE_FEE_MODE = fof_info.incentive_fee_mode
        # FIXME 先hard code
        self._LAST_RAISING_PERIOD_INTEREST_DATE = datetime.date(2020, 12, 20)
        print(f'fof info: (id){FOFDataManager._FOF_ID} (management_fee){self._MANAGEMENT_FEE_PER_YEAR} (custodian_fee){self._CUSTODIAN_FEE_PER_YEAR} '
              f'(admin_service_fee){self._ADMIN_SERVICE_FEE_PER_YEAR} (current_deposit_rate){self._DEPOSIT_INTEREST_PER_YEAR} (subscription_fee){self._SUBSCRIPTION_FEE} '
              f'(incentive fee mode){self._INCENTIVE_FEE_MODE}')

        # 获取FOF份额变化信息
        fof_scale = FOFDataManager.get_fof_scale_alteration([FOFDataManager._FOF_ID])
        self._fof_scale = fof_scale.set_index('datetime')
        self._start_date = self._fof_scale.index.min()

        # trading_day_list = BasicDataApi().get_trading_day_list(start_date=self._start_date, end_date=datetime.datetime.now().date())
        # 将昨天作为end_date
        self._end_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
        print(f'(start_date){self._start_date} (end_date){self._end_date}')
        self._date_list: np.ndarray = pd.date_range(self._start_date, self._end_date).date

        # 获取fof持仓
        positions: Optional[pd.DataFrame] = FOFDataManager.get_fof_asset_allocation([FOFDataManager._FOF_ID])
        assert positions is not None, f'get fof pos for {FOFDataManager._FOF_ID} failed'

        # 这里不需要在途的持仓
        positions = positions[positions.status == FundStatus.DONE]

        positions = positions.pivot(index='confirmed_date', columns=['asset_type', 'fund_id'], values='unit_total')
        positions = positions.reindex(index=self._date_list).ffill()
        # 持仓中的公募基金
        try:
            self._fund_pos = positions[HoldingAssetType.MUTUAL]
        except KeyError:
            print('no fund pos found')

        # 持仓中的私募基金
        try:
            self._hedge_pos = positions[HoldingAssetType.HEDGE]
        except KeyError:
            print('no hedge pos found')

        # 获取私募基金净值数据
        hedge_fund_nav = FOFDataManager.get_hedge_fund_nav()
        hedge_fund_nav = hedge_fund_nav.sort_values(by=['fund_id', 'datetime', 'insert_time']).drop_duplicates(subset=['fund_id', 'datetime'], keep='last')
        self._hedge_nav = hedge_fund_nav.pivot(index='datetime', columns='fund_id', values='v_net_value').reindex(index=self._date_list)

        # 我们自己算一下虚拟净值 然后拿它对_hedge_nav查缺补漏
        v_nav_calcd = self._calc_virtual_net_value()
        # 最后再ffill
        self._hedge_nav = self._hedge_nav.combine_first(v_nav_calcd.reindex(index=self._date_list)).ffill()

        # 获取人工手工校正信息
        manually = BasicDataApi().get_fof_manually([FOFDataManager._FOF_ID])
        self._manually = manually.set_index('datetime')

    def _get_hedge_mv(self) -> float:
        return (self._hedge_nav * self._hedge_pos).round(2).sum(axis=1).fillna(0)

    def _insert_errors_to_db_from_file(self, path: str = ''):
        '''将人工手工校正信息写入DB'''
        if not path:
            path = FOFDataManager._FILE_PATH
        errors: pd.DataFrame = pd.read_excel(path, sheet_name='2-1资产估值表（净值发布）', header=[0, 1, 2], index_col=[0, 1, 2], skipfooter=2)
        errors = errors.loc[:, ['每日管理费误差', '每日行政服务费误差', '每日托管费误差']]
        errors = errors.droplevel(level=[0, 2], axis=0).droplevel(level=[1, 2], axis=1).rename_axis(columns='')
        errors = errors.rename_axis(index=['datetime']).reset_index()
        errors = errors.rename(columns={'每日管理费误差': 'management_fee_error', '每日行政服务费误差': 'admin_service_fee_error', '每日托管费误差': 'custodian_fee_error'})
        errors = errors[errors.notna().any(axis=1)].set_index('datetime').sort_index()

        manually = BasicDataApi().get_fof_manually([FOFDataManager._FOF_ID]).drop(columns='_update_time')
        manually = manually.set_index('datetime')
        manually = manually.combine_first(errors)
        manually['fof_id'] = FOFDataManager._FOF_ID
        manually = manually.reset_index()
        print(manually)
        manually.to_sql(FOFManually.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')

    def _insert_nav_info_to_db_from_file(self, path: str = ''):
        '''将私募基金净值数据写入DB'''
        if not path:
            path = FOFDataManager._FILE_PATH
        nav: pd.DataFrame = pd.read_excel(path, sheet_name=1, header=[0, 1, 2], index_col=[0, 1, 2], skipfooter=2)
        nav = nav.droplevel(level=0)
        nav = nav['私募标的净值']
        nav = nav.loc[(slice(None), 1), :]
        nav = nav.droplevel(level=1)
        nav = nav.stack(0).rename_axis(index=['datetime', 'fund_id'])
        nav = nav.rename(columns={'单位净值': 'net_asset_value', '累计净值': 'acc_unit_value', '虚拟净值': 'v_net_value'})
        nav = nav[nav.notna().any(axis=1)].sort_index(axis=0, level=0).reset_index()
        prog = re.compile('^.*[（(](.*)[）)]$')
        fund_id_list = [prog.search(one) for one in nav.fund_id]
        assert None not in fund_id_list, 'parse hedge fund id failed!!'
        fund_id_list = [one.group(1) for one in fund_id_list]
        nav['fund_id'] = fund_id_list
        print(nav)
        nav.to_sql(HedgeFundNAV.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')

    def _read_data_from_file(self):
        # 解析私募基金净值数据
        nav: pd.DataFrame = pd.read_excel(FOFDataManager._FILE_PATH, sheet_name=1, header=[0, 1, 2], index_col=[0, 1, 2], skipfooter=2)
        nav = nav['私募标的净值']
        nav = nav.swaplevel(axis=1)
        nav = nav['虚拟净值']
        prog = re.compile('^.*[（(](.*)[）)]$')
        fund_id_list = [prog.search(col) for col in nav.columns]
        assert None not in fund_id_list, 'parse hedge fund id failed!!'
        fund_id_list = [one.group(1) for one in fund_id_list]
        nav = nav.set_axis(labels=fund_id_list, axis=1)
        nav = nav.rename_axis(index=['id', 'datetime', 'trading_flag']).reset_index()
        nav = nav[nav.trading_flag == 1]
        nav = nav.drop(columns=['id', 'trading_flag']).set_index('datetime')
        nav = nav.set_axis(pd.to_datetime(nav.index, infer_datetime_format=True).date, axis=0)
        nav = nav[nav.notna().any(axis=1)].sort_index()

        # 解析持仓公募基金数据
        whole_pos: pd.DataFrame = pd.read_excel(FOFDataManager._FILE_PATH, sheet_name=2, header=[0, 1, 2], index_col=[0, 1, 2])
        mutual_fund_pos = whole_pos.loc[:, ('公募标的（份额）', slice(None), '份额')]
        mutual_fund_pos = mutual_fund_pos.droplevel(level=[0, 2], axis=1)
        mutual_fund_pos = mutual_fund_pos.loc[:, mutual_fund_pos.notna().any(axis=0)]
        prog = re.compile('^.*\n[（()](.*)[）)]$')
        fund_id_list = [prog.search(col) for col in mutual_fund_pos.columns]
        assert None not in fund_id_list, 'parse mutual fund id failed!!'
        fund_id_list = [one.group(1) + '!0' for one in fund_id_list]
        mutual_fund_pos = mutual_fund_pos.set_axis(labels=fund_id_list, axis=1)
        mutual_fund_pos = mutual_fund_pos.rename_axis(index=['id', 'datetime', 'trading_flag']).reset_index()
        mutual_fund_pos = mutual_fund_pos[mutual_fund_pos.trading_flag == 1]
        mutual_fund_pos = mutual_fund_pos.drop(columns=['id', 'trading_flag']).set_index('datetime')
        mutual_fund_pos = mutual_fund_pos.set_axis(pd.to_datetime(mutual_fund_pos.index, infer_datetime_format=True).date, axis=0)
        self._fund_pos = mutual_fund_pos[mutual_fund_pos.notna().any(axis=1)].sort_index()
        self._start_date = self._fund_pos.index.min()
        self._end_date = self._fund_pos.index.max()
        print(f'start date: {self._start_date}')
        print(f'end date: {self._end_date}')

        # 解析持仓私募基金数据
        pos: pd.DataFrame = whole_pos.loc[:, '私募标的']
        pos = pos.swaplevel(axis=1)
        pos = pos['份额']
        prog = re.compile('^.*\n[（()](.*)[）)]$')
        fund_id_list = [prog.search(col) for col in pos.columns]
        assert None not in fund_id_list, 'parse hedge fund id failed!!'
        fund_id_list = [one.group(1) for one in fund_id_list]
        pos = pos.set_axis(labels=fund_id_list, axis=1)
        pos = pos.rename_axis(index=['id', 'datetime', 'trading_flag']).reset_index()
        pos = pos[pos.trading_flag == 1]
        pos = pos.drop(columns=['id', 'trading_flag']).set_index('datetime')
        pos = pos.set_axis(pd.to_datetime(pos.index, infer_datetime_format=True).date, axis=0)
        pos = pos[pos.notna().any(axis=1)].sort_index()
        self._hedge_nav = nav
        self._hedge_pos = pos

        # 解析杂项费用、收入数据
        misc_fees: pd.DataFrame = pd.read_excel(FOFDataManager._FILE_PATH, sheet_name=2, header=[0, 1, 2], index_col=[0, 1, 2])
        misc_fees = misc_fees.loc[:, ['银行活期', '在途资金', '累计应收银行\n存款利息', '应收募集期\n利息', '累计计提\n管理费\n（修正）', '累计计提行政\n服务费\n（修正）', '累计计提\n托管费\n（修正）']]
        misc_fees = misc_fees.droplevel(level=[1, 2], axis=1).rename_axis(columns='')
        misc_fees = misc_fees.rename_axis(index=['id', 'datetime', 'trading_flag']).reset_index()
        misc_fees = misc_fees[misc_fees.trading_flag == 1]
        misc_fees = misc_fees.drop(columns=['id', 'trading_flag']).set_index('datetime')
        misc_fees = misc_fees.set_axis(pd.to_datetime(misc_fees.index, infer_datetime_format=True).date, axis=0)
        misc_fees = misc_fees[misc_fees.notna().any(axis=1)].sort_index()
        self._misc_fees = (misc_fees * FOFDataManager._FEES_FLAG).fillna(0).sum(axis=1)

        # 解析投资人持仓数据
        investor_share: pd.DataFrame = pd.read_excel(FOFDataManager._FILE_PATH, sheet_name='4-2投资人份额变更表', header=0, index_col='到账日期', parse_dates=True)
        investor_share = investor_share.rename_axis(index='datetime')
        self._investor_share = investor_share['确认份额'].groupby(level=0).sum().cumsum()

    def calc_nav(self, is_from_excel=False):
        if is_from_excel:
            self._read_data_from_file()
        else:
            self.init()

        # 根据公募基金持仓获取相应基金的净值
        fund_nav: Optional[pd.DataFrame] = BasicDataApi().get_fund_nav_with_date_range(start_date=self._start_date, end_date=self._end_date, fund_list=self._fund_pos.columns.to_list())
        assert fund_nav is not None, f'get fund nav of {self._fund_pos.columns.to_list()} failed'
        fund_nav = fund_nav.pivot(index='datetime', columns='fund_id', values='unit_net_value')
        fund_nav = fund_nav.reindex(index=self._date_list).ffill()
        # 公募基金总市值
        fund_mv: pd.DataFrame = (self._fund_pos * fund_nav).round(2).sum(axis=1).fillna(0)

        if is_from_excel:
            # 净资产 = 公募基金总市值 + 私募基金总市值 + 其他各项收入、费用的净值
            net_assets = fund_mv.add(self._get_hedge_mv(), fill_value=0).add(self._misc_fees, fill_value=0)
            print(net_assets)

            # NAV = 净资产 / 总份额
            investor_share = self._investor_share.reindex(index=net_assets.index).ffill()
            self._fof_nav = net_assets / investor_share
            print(self._fof_nav.round(4))
        else:
            # 获取FOF资产配置信息
            asset_alloc = FOFDataManager.get_fof_asset_allocation([FOFDataManager._FOF_ID])
            asset_alloc = asset_alloc.set_index('datetime')

            hedge_fund_mv = self._get_hedge_mv()

            # 循环遍历每一天来计算
            shares_list = pd.Series(dtype='float64', name='share')
            cash_list = pd.Series(dtype='float64', name='cash')
            fof_nav_list = pd.Series(dtype='float64', name='nav')
            today_fund_mv_list = pd.Series(dtype='float64', name='total_fund_mv')
            today_hedge_mv_list = pd.Series(dtype='float64', name='total_hedge_mv')
            net_assets_list = pd.Series(dtype='float64', name='net_asset')
            net_assets_fixed_list = pd.Series(dtype='float64', name='net_asset_fixed')
            misc_fees_list = pd.Series(dtype='float64', name='misc_fees')
            misc_amount_list = pd.Series(dtype='float64', name='misc_amount')
            deposit_interest_list = pd.Series(dtype='float64', name='deposit_interest')
            positions_list = pd.Series(dtype='float64', name='positions')
            trades_in_transit = []
            deposit_in_transit = []
            total_cash = 0
            for date in self._date_list:
                try:
                    # 看看当天有没有买入FOF
                    # TODO: 暂不支持处理赎回
                    scale_data = self._fof_scale.loc[[date], :]
                except KeyError:
                    # 处理没有买入的情况
                    # 申购金额为0
                    total_amount = 0
                    # 份额增加为0
                    share_increased = 0
                    if not cash_list.empty:
                        # 如果不是计算的第一天，则total_cash到这里仍与头一天相同
                        total_cash = cash_list.iat[-1]
                else:
                    # 汇总今天所有的申购资金
                    total_amount = scale_data.amount.sum()
                    try:
                        # 用申购金额除以确认日的净值以得到份额
                        share_increased = total_amount / (1 + self._SUBSCRIPTION_FEE) / fof_nav_list.at[scale_data.iloc[0, :].confirmed_date]
                    except KeyError:
                        # 没有fof的净值数据，以1作为净值
                        share_increased = total_amount / (1 + self._SUBSCRIPTION_FEE)

                    # 获得银行活期存款
                    if cash_list.empty:
                        # 如果是计算的第一天，认购金额即为银行活期存款
                        total_cash = total_amount
                    else:
                        deposited_date = scale_data.iloc[0, :].deposited_date
                        if date == deposited_date:
                            # 如果和deposited date是同一天，直接将total_amount加到银行活期存款中
                            total_cash = cash_list.iat[-1] + total_amount
                        else:
                            # 如果不是，需要稍后再计算，同时银行活期存款与头一天相同
                            total_cash = cash_list.iat[-1]
                            deposit_in_transit.append((deposited_date, total_amount))
                finally:
                    total_cash = round(total_cash, 2)
                    share_increased = round(share_increased, 2)
                if share_increased > 0:
                    print(f'{self._FOF_ID} share changed (date){date} (amount){total_amount} (share){share_increased}')

                # 这个日期之后才正式成立，所以在此之前都不需要处理后续步骤
                if date < self._ESTABLISHED_DATE:
                    cash_list.loc[date] = total_cash
                    if share_increased > 0:
                        shares_list.loc[date] = share_increased
                    continue

                # 计算那些仍然在途的入金
                deposit_done = []
                deposit_amount_in_transit = 0
                for one in deposit_in_transit:
                    if one[0] == date:
                        # 到了deposited_date，计入银行活期存款然后后续删除该记录
                        deposit_done.append(deposit_in_transit.index(one))
                        total_cash += one[1]
                    else:
                        # 如果没到，也要把他们统计进来，不计算利息，但应该计入净资产中
                        deposit_amount_in_transit += one[1]
                for one in deposit_done:
                    del deposit_in_transit[one]

                try:
                    # 看看当天有没有投出去，继而产生在途资金
                    # TODO: 暂不支持赎回
                    cash_in_transit = 0
                    today_asset_alloc = asset_alloc.loc[[date], :]
                    for row in today_asset_alloc.itertuples():
                        if not pd.isnull(row.amount):
                            cash_in_transit += row.amount
                            if row.confirmed_date != row.Index or row.status == FundStatus.IN_TRANSIT:
                                # 如果没有到confirmed_date或状态是仍然在途，需要把它们记下来
                                trades_in_transit.append((row.Index, row.confirmed_date, row.amount))
                        if not pd.isnull(row.share):
                            # 业绩报酬计提扣除份额完成
                            if row.status == FundStatus.INSENTIVE_DONE:
                                self._hedge_pos.loc[self._hedge_pos.index >= date, row.fund_id] -= row.share
                                # 重刷hedge_fund_mv
                                hedge_fund_mv = self._get_hedge_mv()
                    assert total_cash >= cash_in_transit, f'no enough cash to buy asset!! (date){date} (total cash){total_cash} (cash in transit){cash_in_transit}'
                    total_cash -= cash_in_transit
                except KeyError:
                    cash_in_transit = 0

                # 计算那些仍然在途的资金
                trades_done = []
                for one in trades_in_transit:
                    # 当天就不处理了(在上边处理过了)
                    if one[0] == date:
                        continue
                    if one[1] is not None:
                        if date >= one[1]:
                            # 到confirmed_date了，把这些记录记下来，后续可以删除
                            trades_done.append(trades_in_transit.index(one))
                            # confirmed当天就不把amount计进来了
                            if date == one[1]:
                                continue
                    cash_in_transit += one[2]
                for one in trades_done:
                    del trades_in_transit[one]
                cash_in_transit = round(cash_in_transit, 2)

                # 应收募集期利息 TODO 暂时先hard code了
                if date <= self._LAST_RAISING_PERIOD_INTEREST_DATE:
                    raising_period_interest = 77.78
                else:
                    raising_period_interest = 0
                # 计提管理费, 计提行政服务费, 计提托管费
                if not net_assets_list.empty:
                    misc_fees = (net_assets_list.iat[-1] * pd.Series([self._MANAGEMENT_FEE_PER_YEAR, self._CUSTODIAN_FEE_PER_YEAR, self._ADMIN_SERVICE_FEE_PER_YEAR]) / self._get_days_this_year_for_fee(date)).round(2).sum()
                else:
                    misc_fees = 0

                # 处理人工手工校正的一些数据
                try:
                    fee_transfer = self._manually.at[date, 'fee_transfer']
                    if not pd.isnull(fee_transfer):
                        fee_transfer = round(fee_transfer, 2)
                        # 现金里扣掉的同时 累计计提费用也相应扣掉
                        total_cash += fee_transfer
                        misc_fees += fee_transfer
                except KeyError:
                    pass

                try:
                    other_fees = self._manually.at[date, 'other_fees']
                    if not pd.isnull(other_fees):
                        other_fees = round(other_fees, 2)
                        # 只在现金里扣掉
                        total_cash += other_fees
                except KeyError:
                    pass
                cash_list.loc[date] = total_cash

                # 应收银行存款利息
                deposit_interest = round(cash_list.iat[-1] * self._DEPOSIT_INTEREST_PER_YEAR / self._DAYS_PER_YEAR_FOR_INTEREST, 2)

                try:
                    cd_interest_transfer = self._manually.at[date, 'cd_interest_transfer']
                    if not pd.isnull(cd_interest_transfer):
                        cd_interest_transfer = round(cd_interest_transfer, 2)
                        # 计提费用相应扣掉
                        deposit_interest += cd_interest_transfer
                except KeyError:
                    pass

                # 记录一些信息
                # TODO: 这里也需要在费用划拨时进行相应的扣除
                if deposit_interest_list.empty:
                    deposit_interest_list.loc[date] = deposit_interest
                else:
                    deposit_interest_list.loc[date] = deposit_interest_list.iat[-1] + deposit_interest

                if misc_fees_list.empty:
                    misc_fees_list.loc[date] = misc_fees
                else:
                    misc_fees_list.loc[date] = misc_fees_list.iat[-1] + misc_fees
                misc_amount = total_cash + cash_in_transit + deposit_amount_in_transit + deposit_interest_list.iat[-1] + raising_period_interest - misc_fees_list.iat[-1]
                misc_amount_list.loc[date] = misc_amount

                # 获取持仓中当日公募、私募基金的MV
                try:
                    today_fund_mv = fund_mv.loc[date]
                except KeyError:
                    today_fund_mv = 0
                today_fund_mv_list.loc[date] = today_fund_mv
                try:
                    today_hedge_mv = hedge_fund_mv.loc[date]
                except KeyError:
                    today_hedge_mv = 0
                today_hedge_mv_list.loc[date] = today_hedge_mv
                # 计算净资产
                today_net_assets = today_fund_mv + today_hedge_mv + misc_amount
                net_assets_list.loc[date] = today_net_assets

                try:
                    fund_pos_info = pd.concat([self._fund_pos.loc[date, :].rename('share'), fund_nav.loc[date, :].rename('nav')], axis=1)
                    fund_pos_info = fund_pos_info[fund_pos_info.share.notna()]
                    fund_pos_info['asset_type'] = HoldingAssetType.MUTUAL
                except KeyError:
                    fund_pos_info = None
                try:
                    hedge_pos_info = pd.concat([self._hedge_pos.loc[date, :].rename('share'), self._hedge_nav.loc[date, :].rename('nav')], axis=1)
                    hedge_pos_info = hedge_pos_info[hedge_pos_info.share.notna()]
                    hedge_pos_info['asset_type'] = HoldingAssetType.HEDGE
                except KeyError:
                    hedge_pos_info = None
                if fund_pos_info is not None or hedge_pos_info is not None:
                    position = pd.concat([fund_pos_info, hedge_pos_info], axis=0).rename_axis(index='fund_id').reset_index()
                    positions_list.loc[date] = json.dumps(position.to_dict(orient='records'))

                # 计算修正净资产
                try:
                    errors_to_be_fixed = self._manually.loc[self._manually.index <= date, ['admin_service_fee_error', 'custodian_fee_error', 'management_fee_error']].round(2).sum(axis=1).sum()
                except KeyError:
                    errors_to_be_fixed = 0
                today_net_assets_fixed = today_net_assets + errors_to_be_fixed
                net_assets_fixed_list.loc[date] = today_net_assets_fixed

                # 如果今日有投资人申购fof 记录下来
                if share_increased > 0:
                    shares_list.loc[date] = share_increased
                # 计算fof的nav
                if shares_list.sum() != 0:
                    fof_nav = today_net_assets_fixed / shares_list.sum()
                else:
                    fof_nav = 1
                fof_nav_list.loc[date] = round(fof_nav, 4)
            # 汇总所有信息
            total_info = pd.concat([shares_list, cash_list, fof_nav_list, today_fund_mv_list, today_hedge_mv_list, net_assets_list, net_assets_fixed_list, misc_amount_list, misc_fees_list, deposit_interest_list], axis=1).sort_index()
            print(total_info)
            self._fof_nav = fof_nav_list.rename_axis('datetime').to_frame(name='nav').reset_index()
            self._fof_nav['fof_id'] = FOFDataManager._FOF_ID

            self._fof_position = positions_list.rename_axis('datetime').to_frame(name='position').reset_index()
            self._fof_position['fof_id'] = FOFDataManager._FOF_ID

    def dump_fof_nav_and_pos_to_db(self):
        if self._fof_nav is not None:
            now_df = DerivedDataApi().get_fof_nav([FOFDataManager._FOF_ID])
            if now_df is not None:
                now_df = now_df.drop(columns=['_update_time'])
                # merge on all columns
                df = self._fof_nav.merge(now_df, how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = self._fof_nav
            print(df)
            if not df.empty:
                for date in df.datetime.unique():
                    DerivedDataApi().delete_fof_nav(date_to_delete=date, fof_id_list=df[df.datetime == date].fof_id.to_list())
                df.to_sql(FOFNav.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
                self._wechat_bot.send_fof_nav_update(df)
            print('[dump_fof_nav_and_pos_to_db] dump nav done')
        else:
            print('[dump_fof_nav_and_pos_to_db] no nav, should calc it first')

        if self._fof_position is not None:
            now_df = DerivedDataApi().get_fof_position([FOFDataManager._FOF_ID])
            if now_df is not None:
                now_df = now_df.drop(columns=['_update_time'])
                # merge on all columns
                df = self._fof_position.merge(now_df, how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = self._fof_position
            print(df)
            if not df.empty:
                for date in df.datetime.unique():
                    DerivedDataApi().delete_fof_position(date_to_delete=date, fof_id_list=df[df.datetime == date].fof_id.to_list())
                df.to_sql(FOFPosition.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_and_pos_to_db] dump position done')
        else:
            print('[dump_fof_nav_and_pos_to_db] no position, should calc it first')

    def service_start(self):
        import os
        from ..nav_reader.hedge_fund_nav_reader import HedgeFundNAVReader

        try:
            email_data_dir = os.environ['EMAIL_DATA_DIR']
            user_name = os.environ['EMAIL_USER_NAME']
            password = os.environ['EMAIL_PASSWORD']
        except KeyError as e:
            import sys
            sys.exit(f'[service_start] can not found enough params in env (e){e}')

        hf_nav_r = HedgeFundNAVReader(email_data_dir, user_name, password)
        hf_nav_r.read_navs_and_dump_to_db()
        try:
            self.calc_nav()
            self.dump_fof_nav_and_pos_to_db()
        except Exception as e:
            self._wechat_bot.send_fof_nav_update_failed(self._FOF_ID, f'calc fof nav failed (e){e}')

    @staticmethod
    def _concat_assets_price(main_asset: pd.DataFrame, secondary_asset: pd.Series) -> pd.DataFrame:
        # FIXME 理论上任意资产在任意交易日应该都是有price的 所以这里的判断应该是可以确保之后可以将N种资产的price接起来
        secondary_asset = secondary_asset[secondary_asset.index <= main_asset.datetime.array[0]]
        # 将price对齐
        secondary_asset /= (secondary_asset.array[-1] / main_asset.nav.array[0])
        # 最后一个数据是对齐用的 这里就不需要了
        return pd.concat([main_asset.set_index('datetime'), secondary_asset.iloc[:-1].to_frame('nav')], verify_integrity=True).sort_index().reset_index()

    # 以下是一些获取数据的接口
    @staticmethod
    def get_fof_info(fof_id: Tuple[str] = ()):
        fof_info = BasicDataApi().get_fof_info(fof_id)
        if fof_id is None:
            return
        return fof_info.sort_values(by=['fof_id', 'datetime']).iloc[-1]

    @staticmethod
    def get_fof_asset_allocation(fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_asset_allocation(fof_id)

    @staticmethod
    def get_fof_scale_alteration(fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_scale_alteration(fof_id)

    @staticmethod
    def get_fof_nav(fof_id: str, *, ref_index_id: str = '', ref_fund_id: str = '') -> Optional[pd.DataFrame]:
        fof_nav = DerivedDataApi().get_fof_nav([fof_id])
        if fof_nav is None or fof_nav.empty:
            return
        fof_nav = fof_nav.drop(columns=['_update_time', 'fof_id'])
        if ref_index_id:
            index_price = BasicDataApi().get_index_price(index_list=[ref_index_id])
            if index_price is None or index_price.empty:
                print(f'[get_fof_nav] get price of index {ref_index_id} failed (fof_id){fof_id}')
                return fof_nav
            return FOFDataManager._concat_assets_price(fof_nav, index_price.drop(columns=['_update_time', 'index_id']).set_index('datetime')['close'])
        elif ref_fund_id:
            fund_nav = BasicDataApi().get_fund_nav_with_date(fund_list=[ref_fund_id])
            if fund_nav is None or fund_nav.empty:
                print(f'[get_fof_nav] get nav of fund {ref_fund_id} failed (fof_id){fof_id}')
                return fof_nav
            return FOFDataManager._concat_assets_price(fof_nav, fund_nav.drop(columns='fund_id').set_index('datetime')['adjusted_net_value'])
        else:
            return fof_nav

    @staticmethod
    def get_hedge_fund_info(fund_id: Tuple[str] = ()):
        return BasicDataApi().get_hedge_fund_info(fund_id)

    @staticmethod
    def get_hedge_fund_nav(fund_id: Tuple[str] = ()):
        df = BasicDataApi().get_hedge_fund_nav(fund_id)
        if df is None:
            return
        return df.sort_values(by=['fund_id', 'datetime', 'insert_time']).drop_duplicates(subset=['fund_id', 'datetime'], keep='last')

    @staticmethod
    def get_investor_return(fof_id: str, *, investor_id_list: Tuple[str] = (), start_date: Optional[datetime.date] = None, end_date: Optional[datetime.date] = None) -> Optional[pd.DataFrame]:
        '''计算投资者收益'''

        fof_nav = FOFDataManager().get_fof_nav(fof_id)
        if fof_nav is None:
            return
        fof_scale_info = FOFDataManager().get_fof_scale_alteration([fof_id])
        if fof_scale_info is None:
            return

        fof_nav = fof_nav.set_index('datetime')
        if start_date:
            fof_nav = fof_nav[fof_nav.index >= start_date]
        if end_date:
            fof_nav = fof_nav[fof_nav.index <= end_date]
        investor_mvs = defaultdict(list)
        for row in fof_scale_info.itertuples(index=False):
            if investor_id_list and row.investor_id not in investor_id_list:
                continue
            if start_date is not None:
                actual_start_date = max(row.confirmed_date, start_date)
            else:
                actual_start_date = row.confirmed_date
            try:
                init_mv = fof_nav.at[actual_start_date, 'nav'] * row.unit_total
            except KeyError:
                init_mv = row.unit_total
            try:
                init_water_line = fof_nav.at[row.confirmed_date, 'nav']
            except KeyError:
                init_water_line = 1
            investor_mvs[row.investor_id].append({'start_date': actual_start_date, 'amount': row.amount, 'share': row.unit_total, 'init_mv': init_mv, 'init_water_line': init_water_line})

        investor_returns = {}
        latest_nav = fof_nav.nav.iat[-1]
        for investor_id, datas in investor_mvs.items():
            datas = pd.DataFrame(datas)
            # TODO: hard code 0.2 and 4
            v_nav = FOFDataManager._do_calc_v_net_value(latest_nav, datas.init_water_line, 0.2, 4)
            # 这里确保单取的几个Series的顺序不会发生任何变化 这样直接运算才是OK的
            latest_mv = (v_nav * datas.share).sum()
            total_share = datas.share.sum()
            avg_v_nav = latest_mv / total_share
            total_rr = latest_mv / datas.init_mv.sum() - 1
            investor_returns[investor_id] = {'v_nav': avg_v_nav, 'total_rr': total_rr, 'shares': total_share}
            print(json.dumps([{'fof_id': FOFDataManager._FOF_ID, 'v_nav': avg_v_nav, 'amount': datas.amount.sum(), 'shares': total_share}]))
        return pd.DataFrame.from_dict(investor_returns, orient='index')

    @staticmethod
    def calc_share_by_subscription_amount(fof_id: str, amount: float, confirmed_date: datetime.date) -> Optional[float]:
        '''根据金额和日期计算申购fof产品的确认份额'''

        fof_info: Optional[pd.DataFrame] = FOFDataManager.get_fof_info([fof_id])
        if fof_info is None:
            return
        fof_nav = FOFDataManager().get_fof_nav(fof_id)
        if fof_nav is None:
            return
        try:
            # 用申购金额除以确认日的净值以得到份额
            return amount / (1 + fof_info.subscription_fee) / fof_nav.loc[fof_nav.datetime == confirmed_date, 'nav'].array[-1]
        except KeyError:
            return

    @staticmethod
    def upload_hedge_nav_data(datas: bytes, file_type: str, hedge_fund_id: Tuple[str]) -> bool:
        if file_type == 'csv':
            df = pd.read_csv(io.BytesIO(datas), encoding='gbk')
            df = df.set_axis(['datetime'] + hedge_fund_id, axis=1).set_index('datetime').rename_axis(columns='fund_id')
            df = df.stack().to_frame('adjusted_net_value').reset_index()
            validate = 'many_to_many'
        elif file_type in ('xlsx', 'xls'):
            assert len(hedge_fund_id) == 1, 'error'
            df = pd.read_excel(io.BytesIO(datas), usecols=['净值日期', '净值(分红再投)'], na_values='--')
            df = df.rename(columns={'净值日期': 'datetime', '净值(分红再投)': 'adjusted_net_value'})
            df['fund_id'] = hedge_fund_id[0]
            validate = 'one_to_one'
        else:
            print(f'[upload_hedge_nav_data] can not read data from this type file (file_type){file_type}')
            return False

        now_df = BasicDataApi().get_hedge_fund_nav(hedge_fund_id)
        if now_df is not None:
            now_df = now_df.drop(columns=['_update_time', 'insert_time', 'calc_date']).astype({'net_asset_value': 'float64', 'acc_unit_value': 'float64', 'v_net_value': 'float64'})
            df = df.reindex(columns=now_df.columns).astype(now_df.dtypes.to_dict())
            df['datetime'] = pd.to_datetime(df.datetime, infer_datetime_format=True).dt.date
            # merge on all columns
            df = df.round(6).merge(now_df, how='left', indicator=True, validate=validate)
            df = df[df._merge == 'left_only'].drop(columns=['_merge'])
        if not df.empty:
            for fund_id in df.fund_id.unique():
                BasicDataApi().delete_hedge_fund_nav(fund_id_to_delete=fund_id, date_list=df[df.fund_id == fund_id].datetime.to_list())
            df['insert_time'] = datetime.datetime.now()
            df.to_sql(HedgeFundNAV.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')
            return True
        return False

    @staticmethod
    def virtual_backtest(hedge_fund_id: Tuple[str]) -> pd.DataFrame:
        DEFAULT_INCENTIVE_RATIO = 0.2
        INITIAL_CASH = 10000000
        INIT_NAV = 1
        UNIT_TOTAL = INITIAL_CASH / INIT_NAV

        fund_info = BasicDataApi().get_hedge_fund_info(hedge_fund_id)
        fund_info = fund_info.set_index('fund_id')

        fund_nav = BasicDataApi().get_hedge_fund_nav(hedge_fund_id)
        fund_nav = FOFDataManager._do_calc_v_net_value(fund_nav.pivot(index='datetime', columns='fund_id', values='adjusted_net_value'), fund_info.water_line, fund_info.incentive_fee_ratio.fillna(DEFAULT_INCENTIVE_RATIO), fund_info.v_nav_decimals)
        # FIXME 这里暂时不能直接用数据库里存的虚拟净值 因为这个是邮件里发过来的单位净值虚拟后净值 而上边算出来的是复权净值虚拟后净值
        # fund_nav = fund_nav.pivot(index='datetime', columns='fund_id', values='v_net_value')
        # fund_nav = fund_nav.combine_first(v_nav)

        # 计算虚拟净值
        trading_day = BasicDataApi().get_trading_day_list(start_date=fund_nav.index.array[0], end_date=fund_nav.index.array[-1])
        fund_nav_ffilled = fund_nav.reindex(trading_day.datetime).ffill()
        fund_nav_ffilled = fund_nav_ffilled.loc[:, fund_nav_ffilled.notna().any(axis=0)].loc[fund_nav_ffilled.notna().any(axis=1), :]
        # raw_wgts = [10, 15, 10, 10, 10, 10, 15, 20]
        # wgts = pd.Series(raw_wgts, index=name_dict.values())
        positions = []
        mvs = []
        navs = []
        # 初始市值
        mv = INITIAL_CASH
        print(fund_nav_ffilled)
        for index, s in fund_nav_ffilled.iterrows():
            s = s[s.notna()]
            if positions:
                # 最新市值
                mv = (positions[-1][1] * s).sum()

            if not positions or (s.size != positions[-1][1].size):
                # 调仓
                # new_wgts = wgts.loc[s.index]
                # 各标的目标权重
                # new_wgts /= new_wgts.sum()
                # 新的各标的持仓份数
                # shares = (mv * new_wgts) / s
                shares = (mv / s.size) / s
                positions.append((index, shares))

            nav = mv / UNIT_TOTAL
            mvs.append(mv)
            navs.append(nav)
        fof_nav = pd.Series(navs, index=fund_nav_ffilled.index, name='fof_nav')
        return fof_nav

    # TODO: 提供接口支持对数据的修改


if __name__ == "__main__":
    fof_dm = FOFDataManager()
    fof_dm.service_start()
