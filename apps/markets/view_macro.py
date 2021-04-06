
from surfing.data.api.basic import BasicDataApi
from surfing.data.api.derived import DerivedDataApi
from surfing.data.api.raw import RawDataApi
from surfing.util.calculator import Calculator

from bases.exceptions import LogicError
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan

from .libs import get_title_and_items
from .validators import (TimeValidation, AssetRetValidation, AssetRecentValidation,
                         IndustryRetValidation, IndustryRecentValidation,
                         ProductRetValidation, ProductRecentValidation, ProductCorrValidation)


class AssetMenuAPI(ApiViewHandler):

    @login_required
    def get(self):
        return BasicDataApi().get_asset_details()


class AssetRetAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = AssetRetValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_asset_price(**data)
        if df is None:
            return

        data = Calculator.get_asset_stats(df['_input_asset_nav'], df['_input_asset_info'])
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            'stats': [row.to_dict() for _, row in data.iterrows()]
        }


class AssetRecentAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = AssetRecentValidation.get_valid_data(self.input)
        df = BasicDataApi().asset_recent_rate(**data)
        return get_title_and_items(df)


class IndustryMenuAPI(ApiViewHandler):

    @login_required
    def get(self):
        details = BasicDataApi().get_industry_list()
        return [{'id': industry_id, 'name': industry_name} for industry_id, industry_name in details]


class IndustryRetAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = IndustryRetValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_industry_price(**data)
        if df is None:
            return

        return replace_nan(df.reset_index().to_dict('list'))


class IndustryRecentAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = IndustryRecentValidation.get_valid_data(self.input)
        df = BasicDataApi().industry_recent_rate(**data)
        return get_title_and_items(df)


class ProductMenuAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = []
        details = BasicDataApi().get_product_details()
        for key, value in details.items():
            data.append({
                'title': key,
                'items': [{'id': product_id, 'name': product_name} for product_id, product_name in value],
            })
        return data


class ProductRetAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ProductRetValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_product_price(**data)
        if df is None:
            return

        data = Calculator.get_product_stats(df['_input_asset_nav'], df['_input_asset_info'])
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            'stats': [row.to_dict() for _, row in data.iterrows()]
        }


class ProductRecentAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ProductRecentValidation.get_valid_data(self.input)
        df = BasicDataApi().product_recent_rate(**data)
        return get_title_and_items(df)


class ProductCorrAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ProductCorrValidation.get_valid_data(self.input)
        period = data.pop('period')
        df = BasicDataApi().get_product_price(**data)
        if df is None:
            return

        df = Calculator.get_asset_corr(df['data'], period)
        return get_title_and_items(df)


class FutureDiffAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = TimeValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = RawDataApi().get_stock_index_future_diff(**data)
        return replace_nan(df.reset_index().to_dict('list'))


class MarketSizeAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = TimeValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().market_size_df(**data)
        return replace_nan(df.reset_index().to_dict('list'))


class MainIndexAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = TimeValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_main_index_future_diff_yearly(**data)
        return replace_nan(df.reset_index().to_dict('list'))


class StyleFactorAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = TimeValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = DerivedDataApi().get_style_factor_ret(**data)
        return replace_nan(df.reset_index().to_dict('list'))

