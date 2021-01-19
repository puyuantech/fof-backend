
from typing import Dict, List, Set, Optional
import requests
import json

import pandas as pd

from .config import SurfingConfigurator


class WechatBot(object):

    def __init__(self):
        self.wechat_webhook = SurfingConfigurator().get_wechat_webhook_settings('wechat_webhook')

    def send(self, markdown_content):
        print(markdown_content)
        # Send markdown content
        message = {
            'msgtype': 'markdown',
            'markdown': {
                'content': markdown_content
            }
        }
        res = requests.post(url=self.wechat_webhook, data=json.dumps(message), timeout=20)
        print(res)

    def send_data_update_status(self, dt, failed_tasks, updated_count):
        # Send markdown content
        markdown_content = f'{dt} 已完成数据更新，'
        if len(failed_tasks) == 0:
            markdown_content += '所有数据更新成功'
        else:
            markdown_content += '以下数据更新失败: '
            for key, task_names in failed_tasks.items():
                if len(task_names) > 0:
                    markdown_content += f'\n>{key}: <font color=\"error\">{task_names}</font>'

        markdown_content += '\n更新数据统计: '
        for key, item_count in updated_count.items():
            for item, count in item_count.items():
                markdown_content += f'\n>{key}.{item}: <font color=\"info\">{count}</font>'

        return self.send(markdown_content)

    def send_new_fund_list(self, dt, new_funds: Dict[str, str], new_delisted_funds: Dict[str, str], indexes_that_become_invalid: Optional[Set[str]]):
        markdown_content = f'#### {dt}'
        if new_funds is None or new_delisted_funds is None:
            markdown_content += f' **<font color=\"warning\">获取今日新基金或摘牌基金列表失败</font>**'
        else:
            if new_funds:
                markdown_content += f'\n>新基金({len(new_funds)}): <font color=\"info\">{new_funds}</font>'
            else:
                markdown_content += f'\n>无新基金'
            if new_delisted_funds:
                markdown_content += f'\n\n>摘牌基金({len(new_delisted_funds)}): <font color=\"info\">{new_delisted_funds}</font>'
            else:
                markdown_content += f'\n\n>无摘牌基金'
        if indexes_that_become_invalid is not None and indexes_that_become_invalid:
            markdown_content += f'\n\n\n>**失效指数({len(indexes_that_become_invalid)}, 请注意处理!!): <font color=\"warning\">{indexes_that_become_invalid}</font>**'
        self.send(markdown_content)

    def send_dump_to_s3_result(self, dt, failed_tables: List[str], failed_dfs: List[str]):
        markdown_content = f'#### {dt}'
        if failed_dfs:
            markdown_content += f'\n>**同步下列df失败: <font color=\"warning\">{failed_dfs}</font>**'
        else:
            markdown_content += f'\n><font color=\"info\">同步所有df成功</font>'
        if failed_tables:
            markdown_content += f'\n>**同步下列table失败: <font color=\"warning\">{failed_tables}</font>**'
        else:
            markdown_content += f'\n><font color=\"info\">同步所有table成功</font>'
        self.send(markdown_content)

    def send_update_stock_factor_result(self, dt, failed_factors: List[str]):
        markdown_content = f'#### {dt}'
        if failed_factors:
            markdown_content += f'\n>**更新下列factor失败: <font color=\"warning\">{failed_factors}</font>**'
        else:
            markdown_content += f'\n><font color=\"info\">更新所有factor成功</font>'
        self.send(markdown_content)

    def send_hedge_fund_nav_update(self, df: pd.DataFrame):
        markdown_content = '#### <font color=\"info\">更新以下私募基金净值数据成功</font>'
        markdown_content += f'\n>{df.to_markdown()}'
        self.send(markdown_content)

    def send_hedge_fund_nav_update_failed(self, err_msg: str):
        markdown_content = '#### <font color=\"warning\">更新私募基金净值数据错误！！</font>'
        markdown_content += f'\n>**err msg:** {err_msg}'
        self.send(markdown_content)

    def send_fof_nav_update(self, df):
        markdown_content = f'#### <font color=\"info\">FOF净值数据更新</font>'
        markdown_content += f'\n>**{df.to_markdown()}**'
        self.send(markdown_content)

    def send_fof_nav_update_failed(self, fof_id: str, err_msg: str):
        markdown_content = f'#### <font color=\"info\">{fof_id}净值数据更新失败！！</font>'
        markdown_content += f'\n>**err msg:** {err_msg}'
        self.send(markdown_content)

    def send_refinancing_key_info(self, dt, stocks, key):
        if stocks:
            markdown_content = f'#### {dt}'
            markdown_content += f'\n下列上市公司发布再融资预案，发行对象中包括 **<font color=\"warning\">{key}</font>**'
            markdown_content += f'\n>**<font color=\"info\">{stocks}</font>**'
            self.send(markdown_content)

    def send_refinancing_impl_key_info(self, dt, stocks, key):
        if stocks:
            markdown_content = f'#### {dt}'
            markdown_content += f'\n下列上市公司发布再融资实施公告，获配对象中包括 **<font color=\"warning\">{key}</font>**'
            markdown_content += f'\n>**<font color=\"info\">{stocks}</font>**'
            self.send(markdown_content)
