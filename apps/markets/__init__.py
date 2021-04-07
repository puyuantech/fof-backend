from flask import Blueprint
from flask_restful import Api
from .view import IndexListAPI, IndexAPI, IndexDetailAPI, IndexSingleChangeAPI
from .view_macro import (AssetMenuAPI, AssetRetAPI, AssetRecentAPI,
                         IndustryMenuAPI, IndustryRetAPI, IndustryRecentAPI,
                         ProductMenuAPI, ProductRetAPI, ProductRecentAPI, ProductCorrAPI,
                         FutureDiffAPI, MarketSizeAPI, MainIndexAPI, StyleFactorAPI,
                         ValuationMenuAPI, ValuationIndexAPI, ValuationIndustryAPI,
                         ValuationHistoryAPI, StockRetAPI)

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/market')
api = Api(blu)

api.add_resource(IndexListAPI, '')
api.add_resource(IndexAPI, '/<int:_id>')
api.add_resource(IndexDetailAPI, '/detail/<int:_id>')
api.add_resource(IndexSingleChangeAPI, '/single_change')

api.add_resource(AssetMenuAPI, '/macro/asset/menu')
api.add_resource(AssetRetAPI, '/macro/asset/ret')
api.add_resource(AssetRecentAPI, '/macro/asset/recent')
api.add_resource(IndustryMenuAPI, '/macro/industry/menu')
api.add_resource(IndustryRetAPI, '/macro/industry/ret')
api.add_resource(IndustryRecentAPI, '/macro/industry/recent')
api.add_resource(ProductMenuAPI, '/macro/product/menu')
api.add_resource(ProductRetAPI, '/macro/product/ret')
api.add_resource(ProductRecentAPI, '/macro/product/recent')
api.add_resource(ProductCorrAPI, '/macro/product/corr')
api.add_resource(FutureDiffAPI, '/macro/future_diff')
api.add_resource(MarketSizeAPI, '/macro/market_size')
api.add_resource(MainIndexAPI, '/macro/main_index')
api.add_resource(StyleFactorAPI, '/macro/style_factor')
api.add_resource(ValuationMenuAPI, '/macro/valuation/menu')
api.add_resource(ValuationIndexAPI, '/macro/valuation/index')
api.add_resource(ValuationIndustryAPI, '/macro/valuation/industry')
api.add_resource(ValuationHistoryAPI, '/macro/valuation/history')
api.add_resource(StockRetAPI, '/macro/stock_ret')
