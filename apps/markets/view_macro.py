
from collections import defaultdict

from surfing.data.api.basic import BasicDataApi
from surfing.data.api.derived import DerivedDataApi
from surfing.data.api.raw import RawDataApi
from surfing.util.calculator import Calculator

from bases.exceptions import LogicError
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan

from .libs import get_title_and_items
from .validators import (TimeValidation, AssetRetValidation, AssetRecentValidation, IndustryRetValidation,
                         IndustryRecentValidation, ProductRetValidation, ProductRecentValidation,
                         ProductCorrValidation, ProductRollingValidation, ValuationTimeValidation,
                         ValuationIndexValidation, ValuationIndustryValidation, ValuationHistoryValidation,
                         StockDebtValidation, SideCapValidation, AHPremValidation)


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

        stats = Calculator.get_asset_stats(df['_input_asset_nav'], df['_input_asset_info'])
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            'stats': [row.to_dict() for _, row in stats.iterrows()]
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

        stats = Calculator.get_product_stats(df['_input_asset_nav'], df['_input_asset_info'])
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            'stats': [row.to_dict() for _, row in stats.iterrows()]
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


class ProductBenchmarkAPI(ApiViewHandler):

    @login_required
    def get(self):
        return BasicDataApi().get_product_benchmark()


class ProductRollingCorrAPI(ApiViewHandler):

    @login_required
    def post(self):
        params = ProductRollingValidation.get_valid_data(self.input)
        data = ProductRetValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_product_price(**data)
        if df is None:
            return

        df = Calculator.get_product_rolling_corr(df['_input_asset_nav'], **params)
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            'stats': {key: get_title_and_items(value) for key, value in df['details'].items()}
        }


class ProductRollingBetaAPI(ApiViewHandler):

    @login_required
    def post(self):
        params = ProductRollingValidation.get_valid_data(self.input)
        data = ProductRetValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_product_price(**data)
        if df is None:
            return

        df = Calculator.get_product_rolling_beta(df['_input_asset_nav'], **params)
        return replace_nan(df.reset_index().to_dict('list'))


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


class ValuationMenuAPI(ApiViewHandler):

    @login_required
    def get(self):
        return DerivedDataApi().get_index_val_info()


class ValuationIndexAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ValuationIndexValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = DerivedDataApi().get_index_valuation_with_period(**data)

        data.pop('valuation_type')
        stats = Calculator.get_index_stats(**data)
        return {
            'indexs': replace_nan(df['data'].reset_index().to_dict('list')),
            'stats': replace_nan([row.to_dict() for _, row in stats.iterrows()])
        }


class ValuationIndustryAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ValuationIndustryValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = DerivedDataApi().get_all_industry_val(**data)
        return {
            '散点': df['散点'].reset_index().to_dict('list'),
            '虚线': df['虚线'].reset_index().to_dict('list'),
        }


class ValuationHistoryAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ValuationHistoryValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = Calculator.index_val_history(**data)
        return replace_nan(df.reset_index().to_dict('list'))


class StockRetAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = TimeValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = DerivedDataApi().get_industry_stock_ret_and_size(**data)

        industry_1_data = df['行业一级收益'].reset_index().to_dict('records')

        industry_2_data = defaultdict(list)
        for row in df['行业二级收益'].reset_index().to_dict('records'):
            industry_2_data[row['industry_1']].append(row)

        stock_data = defaultdict(list)
        for row in df['股票收益'].drop(columns=['industry_1', 'industry_1_name', 'industry_2_name']).reset_index().to_dict('records'):
            stock_data[row['industry_2']].append(row)

        return {
            '行业一级收益': industry_1_data,
            '行业二级收益': industry_2_data,
            '股票收益': stock_data,
        }


class StockDebtMenuAPI(ApiViewHandler):

    @login_required
    def get(self):
        return DerivedDataApi().stock_debt_val_info()


class StockDebtDetailAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = StockDebtValidation.get_valid_data(self.input)
        df = DerivedDataApi().stock_debt_val_detail(**data)
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            'title': df['title'],
        }


class IndustryBetaAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ValuationTimeValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = DerivedDataApi().industry_beta(**data)
        return replace_nan(df.reset_index().to_dict('list'))


class SideCapAPI(ApiViewHandler):

    @login_required
    def get(self):
        return BasicDataApi().get_side_cap_index()

    @login_required
    def post(self):
        data = SideCapValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_side_cap_data(**data)
        return replace_nan(df.reset_index().to_dict('list'))


class PPIAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ValuationTimeValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_ppi(**data)
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            '沪深300总增长': df['沪深300总增长'],
            '介绍': df['介绍'],
        }


class PMIAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ValuationTimeValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_pmi(**data)
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            '介绍': df['介绍'],
        }


class GDPAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ValuationTimeValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_gdp(**data)
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            '介绍': df['text'],
        }


class CPIAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ValuationTimeValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_cpi(**data)
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            '介绍': df['text'],
        }


class USBondAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ValuationTimeValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_us_bond_rate(**data)
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            '介绍': df['text'],
        }


class USDIndexAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ValuationTimeValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_usd_index(**data)
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            '介绍': df['text'],
        }


class AHPremAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = AHPremValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_ah_prem(**data)
        return replace_nan(df['data'].reset_index().to_dict('list'))


class RzrqyeAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = TimeValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        df = BasicDataApi().get_rzrqye(**data)
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            '介绍': df['text'],
        }

