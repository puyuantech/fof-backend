
from bases.validation import BaseValidation
from bases.viewhandler import ApiViewHandler
from pydantic import conlist
from surfing.data.api.basic import BasicDataApi
from utils.decorators import login_required
from utils.helper import replace_nan


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


class RetValidation(BaseValidation):
    asset_list: conlist(str, min_items=1)


class MacroRetAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = RetValidation.get_valid_data(self.input)
        df = BasicDataApi().get_asset_price(data['asset_list'])
        if df is None:
            return
        return replace_nan(df.reset_index().rename(columns={'index':'datetime'}).to_dict('list'))

