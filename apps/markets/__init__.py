from flask import Blueprint
from flask_restful import Api
from .view import IndexListAPI, IndexAPI, IndexDetailAPI, IndexSingleChangeAPI
from .view_macro import MacroMenuAPI, MacroRetAPI, MacroRecentAPI, FutureDiffAPI, MarketSizeAPI, MainIndexAPI, StyleFactorAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/market')
api = Api(blu)

api.add_resource(IndexListAPI, '')
api.add_resource(IndexAPI, '/<int:_id>')
api.add_resource(IndexDetailAPI, '/detail/<int:_id>')
api.add_resource(IndexSingleChangeAPI, '/single_change')

api.add_resource(MacroMenuAPI, '/macro/menu')
api.add_resource(MacroRetAPI, '/macro/ret')
api.add_resource(MacroRecentAPI, '/macro/recent')
api.add_resource(FutureDiffAPI, '/macro/future_diff')
api.add_resource(MarketSizeAPI, '/macro/market_size')
api.add_resource(MainIndexAPI, '/macro/main_index')
api.add_resource(StyleFactorAPI, '/macro/style_factor')
