
import json

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from models import PortfolioTrade
from utils.helper import json_str_to_dict


class ProductionInfoCas(Model):
    __table_name__ = 'production_info_cas'
    __keyspace__ = 'fof'

    manager_id = columns.Text(primary_key=True)
    portfolio_id = columns.Integer(primary_key=True)
    portfolio_name = columns.Text()
    create_time = columns.DateTime()
    update_time = columns.DateTime()
    port_status = columns.Text()
    port_asset_weight = columns.Text()
    port_fund_weight = columns.Text()

    def to_dict(self):
        return {
            'manager_id': self.manager_id,
            'portfolio_id': self.portfolio_id,
            'portfolio_name': self.portfolio_name,
            'create_time': self.create_time,
            'update_time': self.update_time,
            'port_status': json_str_to_dict(self.port_status),
            'port_asset_weight': json_str_to_dict(self.port_asset_weight),
            'port_fund_weight': json_str_to_dict(self.port_fund_weight),
        }

    @classmethod
    def create_info(cls, portfolio_trade: PortfolioTrade, portfolio_info):
        cls.create(
            manager_id=portfolio_trade.manager_id,
            portfolio_id=portfolio_trade.id,
            portfolio_name=portfolio_trade.portfolio_name,
            create_time=portfolio_trade.create_time,
            update_time=portfolio_trade.update_time,
            port_status=json.dumps(portfolio_info['port_status']),
            port_asset_weight=json.dumps(portfolio_info['port_asset_weight']),
            port_fund_weight=json.dumps(portfolio_info['port_fund_weight']),
        )

    @classmethod
    def update_info(cls, portfolio_trade: PortfolioTrade, portfolio_info, update_time):
        cls.get(
            manager_id=portfolio_trade.manager_id,
            portfolio_id=portfolio_trade.id,
        ).update(
            portfolio_name=portfolio_trade.portfolio_name,
            update_time=update_time,
            port_status=json.dumps(portfolio_info['port_status']),
            port_asset_weight=json.dumps(portfolio_info['port_asset_weight']),
            port_fund_weight=json.dumps(portfolio_info['port_fund_weight']),
        )

