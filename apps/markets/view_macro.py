
from surfing.data.api.basic import BasicDataApi
from surfing.util.calculator import Calculator

from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan

from .validators import RetValidation, RecentValidation


class MacroMenuAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = []
        asset_details = BasicDataApi().get_asset_details()
        for key in ('大类资产', '股票指数', '期货指数', '典型产品', '策略指数'):

            data.append({
                'title': key,
                'items': [{'id': asset_id, 'name': asset_name} for asset_id, asset_name in asset_details[key]],
            })
        return data


class MacroRetAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = RetValidation.get_valid_data(self.input)
        df = BasicDataApi().get_asset_price(data['asset_list'])
        if df is None:
            return
        data = Calculator.get_asset_stats(df['_input_asset_nav'], df['_input_asset_info'])
        return {
            'rets': replace_nan(df['data'].reset_index().rename(columns={'index':'datetime'}).to_dict('list')),
            'stats': [row.to_dict() for _, row in data.iterrows()]
        }


class MacroRecentAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = RecentValidation.get_valid_data(self.input)
        df = BasicDataApi().asset_recent_rate(**data)
        df = df.reset_index().to_dict('list')
        return {
            'title': df.pop('index_id'),
            'items': [{'key': k, 'value': v} for k, v in df.items()],
        }

