from bases.dbwrapper import db, BaseModel
from sqlalchemy.dialects.mysql import DOUBLE


class CustomIndex(BaseModel):
    """
    自定义指数
    """
    __tablename__ = 'custom_index'

    id = db.Column(db.Integer, primary_key=True)                                # 编号
    name = db.Column(db.String(31))                                             # 名称
    desc = db.Column(db.String(255))                                            # 描述
    recent_1m_ret = db.Column(DOUBLE(asdecimal=False))                           # 最近1月收益
    recent_3m_ret = db.Column(DOUBLE(asdecimal=False))                          # 最近3月收益
    recent_6m_ret = db.Column(DOUBLE(asdecimal=False))                          # 最近6月收益
    recent_y1_ret = db.Column(DOUBLE(asdecimal=False))                          # 近一年收益
    recent_y3_ret = db.Column(DOUBLE(asdecimal=False))                          # 近三年收益
    recent_y5_ret = db.Column(DOUBLE(asdecimal=False))                          # 近五年收益
    mdd = db.Column(DOUBLE(asdecimal=False))                                    # 最大回撤
    sharpe = db.Column(DOUBLE(asdecimal=False))                                 # 夏普比率
    last_unit_nav = db.Column(DOUBLE(asdecimal=False))                          # 最新净值
    annualized_ret = db.Column(DOUBLE(asdecimal=False))                         # 年化收益
    annualized_vol = db.Column(DOUBLE(asdecimal=False))                         # 年化波动率
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)


class CustomIndexNav(BaseModel):
    """
    净值
    """
    __tablename__ = 'custom_index_nav'

    id = db.Column(db.Integer, primary_key=True)                                # 编号
    index_id = db.Column(db.Integer)                                            # 指数ID
    datetime = db.Column(db.Date)                                               # 日期
    nav = db.Column(DOUBLE(asdecimal=False))                                    # 净值
