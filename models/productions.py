from bases.dbwrapper import db, BaseModel
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy import Index


class FOFInfo(BaseModel):
    """
    产品
    """
    __tablename__ = 'fof_info'

    fof_id = db.Column(db.CHAR(16), primary_key=True)                                   # 产品ID
    datetime = db.Column(db.CHAR(16), primary_key=True)                                 # 数据日期（以支持更新操作）
    fof_name = db.Column(db.TEXT, nullable=False)                                       # 产品名称
    admin = db.Column(db.TEXT, nullable=False)                                          # 管理人
    established_date = db.Column(db.DATE, nullable=False)                               # 成立日期
    fof_status = db.Column(db.TEXT, nullable=False)                                     # 申赎状态等
    subscription_fee = db.Column(DOUBLE(asdecimal=False), nullable=False)               # 认购费率
    redemption_fee = db.Column(DOUBLE(asdecimal=False), nullable=False)                 # 赎回费率
    management_fee = db.Column(DOUBLE(asdecimal=False), nullable=False)                 # 管理费率
    custodian_fee = db.Column(DOUBLE(asdecimal=False), nullable=False)                  # 托管费率
    administrative_fee = db.Column(DOUBLE(asdecimal=False), nullable=False)             # 行政管理费率
    lock_up_period = db.Column(db.TEXT, nullable=False)                                 # 锁定期
    incentive_fee_mode = db.Column(db.TEXT, nullable=False)                             # 业绩报酬计提方法
    incentive_fee = db.Column(db.TEXT, nullable=False)                                  # 业绩报酬提取比例
    current_deposit_rate = db.Column(DOUBLE(asdecimal=False), nullable=False)           # 银行活期存款利率
    initial_raised_fv = db.Column(DOUBLE(asdecimal=False), nullable=False)              # 净值
    initial_net_value = db.Column(DOUBLE(asdecimal=False), nullable=False)              # 总资产


class FOFScaleAlteration(BaseModel):
    """
    规模变动记录
    """

    __tablename__ = 'fof_scale_alteration'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fof_id = db.Column(db.CHAR(16), primary_key=True)                                   # 产品ID
    datetime = db.Column(db.DATE, primary_key=True)                                     # 日期
    confirmed_date = db.Column(db.DATE)                                                 # 确认日期
    deposited_date = db.Column(db.DATE)                                                 # 入账日期
    amount = db.Column(DOUBLE(asdecimal=False))                                         # 被申购金额
    share = db.Column(DOUBLE(asdecimal=False))                                          # 被赎回份额


class FOFAssetAllocation(BaseModel):
    """
    fof资产配置记录
    """

    __tablename__ = 'fof_asset_allocation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fof_id = db.Column(db.CHAR(16), primary_key=True)                                   # 产品ID
    datetime = db.Column(db.DATE, primary_key=True)                                     # 日期
    fund_id = db.Column(db.CHAR(16), primary_key=True, nullable=False)                  # 申购/赎回基金ID
    asset_type = db.Column(db.String(31), nullable=False)                               # 资产类型
    amount = db.Column(DOUBLE(asdecimal=False))                                         # 申购金额
    share = db.Column(DOUBLE(asdecimal=False))                                          # 赎回份额
    status = db.Column(db.String(31), nullable=False)                                   # 状态：在途/完成
    confirmed_date = db.Column(db.DATE)                                                 # 确认日期
    unit_total = db.Column(DOUBLE(asdecimal=False))                                     # 确认份额
    trade_type = db.Column(db.BOOLEAN)                                                  # 交易类型 buy/sell


class FOFManually(BaseModel):
    """
    fof手工校正数据
    """

    __tablename__ = 'fof_manually'

    fof_id = db.Column(db.CHAR(16), primary_key=True)                                   # 产品ID
    datetime = db.Column(db.DATE, primary_key=True)                                     # 日期
    fee_transfer = db.Column(DOUBLE(asdecimal=False))                                   # 费用划拨
    cd_interest_transfer = db.Column(DOUBLE(asdecimal=False))                           # 银行活期存款利息扣除
    other_fees = db.Column(DOUBLE(asdecimal=False))                                     # 其他费用划拨
    management_fee_error = db.Column(DOUBLE(asdecimal=False))                           # 管理费误差
    custodian_fee_error = db.Column(DOUBLE(asdecimal=False))                            # 托管费误差
    admin_service_fee_error = db.Column(DOUBLE(asdecimal=False))                        # 行政服务费误差


class FOFNav(BaseModel):
    """
    fof净值数据
    """

    __tablename__ = 'fof_nav'

    fof_id = db.Column(db.CHAR(16), primary_key=True)                                   # 产品ID
    datetime = db.Column(db.DATE, primary_key=True)                                     # 日期
    nav = db.Column(DOUBLE(asdecimal=False), nullable=False)                            # 单位净值


class FOFPosition(BaseModel):
    """
    fof净值数据
    """

    __tablename__ = 'fof_position'

    fof_id = db.Column(db.CHAR(16), primary_key=True)                                   # 产品ID
    datetime = db.Column(db.DATE, primary_key=True)                                     # 日期
    position = db.Column(db.TEXT)                                                       # 持仓


class HedgeFundNAV(BaseModel):
    """
    私募基金净值
    """

    __tablename__ = 'hedge_fund_nav'

    fund_id = db.Column(db.CHAR(16), primary_key=True)                                  # 基金ID
    datetime = db.Column(db.DATE, primary_key=True)                                     # 日期
    insert_time = db.Column(db.DATETIME, primary_key=True)                              # 插入时间
    calc_date = db.Column(db.DATE)                                                      # 计算日期
    net_asset_value = db.Column(DOUBLE(asdecimal=False), nullable=False)                # 单位净值
    acc_unit_value = db.Column(DOUBLE(asdecimal=False))                                 # 累计净值
    v_net_value = db.Column(DOUBLE(asdecimal=False))                                    # 虚拟净值

    __table_args__ = (
        Index('idx_hedge_fund_nav_datetime', 'datetime'),
    )


class HedgeFundInfo(BaseModel):
    """
    私募基金信息
    """

    __tablename__ = 'hedge_fund_info'

    fund_id = db.Column(db.CHAR(16), primary_key=True)                                  # 基金ID
    fund_name = db.Column(db.TEXT, nullable=False)                                      # 基金名称
    manager_id = db.Column(db.CHAR(16), nullable=False)                                 # 私募基金公司ID
    manager = db.Column(db.String(31))                                                  # 基金经理
    size = db.Column(DOUBLE(asdecimal=False))                                           # 基金规模
    water_line = db.Column(DOUBLE(asdecimal=False), nullable=False)                     # 水位线
    incentive_fee_mode = db.Column(db.TEXT, nullable=False)                             # 业绩报酬计提方法
    incentive_fee_ratio = db.Column(DOUBLE(asdecimal=False), nullable=False)            # 业绩计提比例
    v_nav_decimals = db.Column(db.SMALLINT, nullable=False)                             # 虚拟净值精度
    stars = db.Column(db.Integer, default=1)                                            # 星级
    net_asset_value = db.Column(DOUBLE(asdecimal=False))                                # 单位净值
    acc_unit_value = db.Column(DOUBLE(asdecimal=False))                                 # 累计净值
    v_net_value = db.Column(DOUBLE(asdecimal=False))                                    # 虚拟净值


class HedgeComment(BaseModel):
    """
    私募评论
    """
    __tablename__ = 'hedge_comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fund_id = db.Column(db.CHAR(16), db.ForeignKey('hedge_fund_info.fund_id'))
    fund = db.relationship('HedgeFundInfo', backref='comments')
    comment = db.Column(db.String(255))                                                 # 评论


