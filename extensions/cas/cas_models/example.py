from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from utils.helper import json_str_to_dict


class CasExample(Model):
    __table_name__ = 'examples'
    __keyspace__ = 'fof'

    user_id = columns.Integer(primary_key=True)        # 用户ID
    time_stamp = columns.Text(primary_key=True)        # 方案ID
    rate = columns.Text()                              # 比率信息
    create_time = columns.DateTime()                   # 创建时间
    update_time = columns.DateTime()                   # 更新时间

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'time_stamp': self.time_stamp,
            'rate': json_str_to_dict(self.rate),
            'create_time': self.create_time,
            'update_time': self.update_time,
        }
