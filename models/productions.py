from bases.dbwrapper import BaseModel
from sqlalchemy.dialects.mysql import DOUBLE, TEXT, CHAR, INTEGER, DATE, DATETIME, BOOLEAN, SMALLINT, VARCHAR
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Index


# class FOFInfo(BaseModel):
#     """
#     产品
#     """
#     __tablename__ = 'fof_info'
#
#     fof_id = Column(CHAR(16), primary_key=True)                                   # 产品ID
#     datetime = Column(CHAR(16), primary_key=True)                                 # 数据日期（以支持更新操作）
#     fof_name = Column(TEXT, nullable=False)                                       # 产品名称
#     admin = Column(TEXT, nullable=False)                                          # 管理人
#     established_date = Column(DATE, nullable=False)                               # 成立日期
#     fof_status = Column(TEXT, nullable=False)                                     # 申赎状态等
#     subscription_fee = Column(DOUBLE(asdecimal=False), nullable=False)               # 认购费率
#     redemption_fee = Column(DOUBLE(asdecimal=False), nullable=False)                 # 赎回费率
#     management_fee = Column(DOUBLE(asdecimal=False), nullable=False)                 # 管理费率
#     custodian_fee = Column(DOUBLE(asdecimal=False), nullable=False)                  # 托管费率
#     administrative_fee = Column(DOUBLE(asdecimal=False), nullable=False)             # 行政管理费率
#     lock_up_period = Column(TEXT, nullable=False)                                 # 锁定期
#     incentive_fee_mode = Column(TEXT, nullable=False)                             # 业绩报酬计提方法
#     incentive_fee = Column(TEXT, nullable=False)                                  # 业绩报酬提取比例
#     current_deposit_rate = Column(DOUBLE(asdecimal=False), nullable=False)           # 银行活期存款利率
#     initial_raised_fv = Column(DOUBLE(asdecimal=False), nullable=False)              # 净值
#     initial_net_value = Column(DOUBLE(asdecimal=False), nullable=False)              # 总资产


# class FOFScaleAlteration(BaseModel):
#     """
#     规模变动记录
#     """
#
#     __tablename__ = 'fof_scale_alteration'
#
#     id = Column(INTEGER, primary_key=True, autoincrement=True)
#     fof_id = Column(CHAR(16), primary_key=True)                                   # 产品ID
#     datetime = Column(DATE, primary_key=True)                                     # 日期
#     confirmed_date = Column(DATE)                                                 # 确认日期
#     deposited_date = Column(DATE)                                                 # 入账日期
#     amount = Column(DOUBLE(asdecimal=False))                                         # 被申购金额
#     share = Column(DOUBLE(asdecimal=False))                                          # 被赎回份额


# class FOFAssetAllocation(BaseModel):
#     """
#     fof资产配置记录
#     """
#
#     __tablename__ = 'fof_asset_allocation'
#
#     id = Column(INTEGER, primary_key=True, autoincrement=True)
#     fof_id = Column(CHAR(16), primary_key=True)                                   # 产品ID
#     investor_id = Column(CHAR(20))                                                # 投资者ID
#     datetime = Column(DATE, primary_key=True)                                     # 日期
#     fund_id = Column(CHAR(16), primary_key=True, nullable=False)                  # 申购/赎回基金ID
#     asset_type = Column(CHAR(31), nullable=False)                               # 资产类型
#     amount = Column(DOUBLE(asdecimal=False))                                         # 申购金额
#     share = Column(DOUBLE(asdecimal=False))                                          # 赎回份额
#     status = Column(CHAR(31), nullable=False)                                   # 状态：在途/完成
#     confirmed_date = Column(DATE)                                                 # 确认日期
#     unit_total = Column(DOUBLE(asdecimal=False))                                     # 确认份额
#     trade_type = Column(BOOLEAN)                                                  # 交易类型 buy/sell
#

# class FOFManually(BaseModel):
#     """
#     fof手工校正数据
#     """
#
#     __tablename__ = 'fof_manually'
#
#     fof_id = Column(CHAR(16), primary_key=True)                                   # 产品ID
#     datetime = Column(DATE, primary_key=True)                                     # 日期
#     fee_transfer = Column(DOUBLE(asdecimal=False))                                   # 费用划拨
#     cd_interest_transfer = Column(DOUBLE(asdecimal=False))                           # 银行活期存款利息扣除
#     other_fees = Column(DOUBLE(asdecimal=False))                                     # 其他费用划拨
#     management_fee_error = Column(DOUBLE(asdecimal=False))                           # 管理费误差
#     custodian_fee_error = Column(DOUBLE(asdecimal=False))                            # 托管费误差
#     admin_service_fee_error = Column(DOUBLE(asdecimal=False))                        # 行政服务费误差


# class FOFNav(BaseModel):
#     """
#     fof净值数据
#     """
#
#     __tablename__ = 'fof_nav'
#
#     fof_id = Column(CHAR(16), primary_key=True)                                   # 产品ID
#     datetime = Column(DATE, primary_key=True)                                     # 日期
#     nav = Column(DOUBLE(asdecimal=False), nullable=False)                            # 单位净值
#
#
# class FOFPosition(BaseModel):
#     """
#     fof净值数据
#     """
#
#     __tablename__ = 'fof_position'
#
#     fof_id = Column(CHAR(16), primary_key=True)                                   # 产品ID
#     datetime = Column(DATE, primary_key=True)                                     # 日期
#     position = Column(TEXT)                                                       # 持仓





# class HedgeFundInfo(BaseModel):
#     """
#     私募基金信息
#     """
#
#     __tablename__ = 'hedge_fund_info'
#
#     fund_id = Column(CHAR(16), primary_key=True)                                  # 基金ID
#     fund_name = Column(TEXT, nullable=False)                                      # 基金名称
#     manager_id = Column(CHAR(16), nullable=False)                                 # 私募基金公司ID
#     manager = Column(CHAR(31))                                                  # 基金经理
#     size = Column(DOUBLE(asdecimal=False))                                           # 基金规模
#     water_line = Column(DOUBLE(asdecimal=False), nullable=False)                     # 水位线
#     incentive_fee_mode = Column(TEXT, nullable=False)                             # 业绩报酬计提方法
#     incentive_fee_ratio = Column(DOUBLE(asdecimal=False), nullable=False)            # 业绩计提比例
#     v_nav_decimals = Column(SMALLINT, nullable=False)                             # 虚拟净值精度
#     stars = Column(INTEGER, default=1)                                            # 星级
#     net_asset_value = Column(DOUBLE(asdecimal=False))                                # 单位净值
#     acc_unit_value = Column(DOUBLE(asdecimal=False))                                 # 累计净值
#     v_net_value = Column(DOUBLE(asdecimal=False))                                    # 虚拟净值


class HedgeComment(BaseModel):
    """
    私募评论
    """
    __tablename__ = 'hedge_comments'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    fund_id = Column(CHAR(16))
    comment = Column(VARCHAR(255))                                                 # 评论


# class InvestorPosition(BaseModel):
#     """
#     产品
#     """
#     __tablename__ = 'user_positions'
#
#     id = Column(INTEGER, primary_key=True, autoincrement=True)
#     investor_id = Column(CHAR(16))
#     fof_id = Column(CHAR(16))
#     amount = Column(DOUBLE(asdecimal=False))
#     shares = Column(DOUBLE(asdecimal=False))
#     datetime = Column(DATE)
#     asset_type = Column(CHAR(10))

