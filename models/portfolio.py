
from bases.dbwrapper import db, BaseModel


class PortfolioTrade(BaseModel):
    """组合交易记录"""
    __tablename__ = 'portfolio_trade'

    id = db.Column(db.Integer, primary_key=True)
    portfolio_name = db.Column(db.String(32))
    manager_id = db.Column(db.String(32))
    trade_history = db.Column(db.JSON)
    benchmark_info = db.Column(db.JSON)

    @property
    def benchmark_id_info(self):
        return {benchmark['asset_name']: benchmark['index_id'] for benchmark in self.benchmark_info}

