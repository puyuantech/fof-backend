
import pandas as pd
import empyrical as ep
from flask import request

from extensions.es.es_searcher import IndexSearcher
from extensions.es.es_conn import ElasticSearchConnector
from extensions.es.es_models import IndexSearchDoc
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.queries import SurfingQuery
from utils.helper import replace_nan


class IndexSearcherAPI(ApiViewHandler):

    @login_required
    def get(self, key_word):
        page = int(request.args.get('page', 0))
        page_size = int(request.args.get('page_size', 5))
        offset = page * page_size

        conn = ElasticSearchConnector().get_conn()
        searcher = IndexSearcher(conn, key_word, IndexSearchDoc)
        results, count = searcher.get_usually_query_result(key_word, offset, page_size)
        results = [[i.order_book_id, i.desc_name, i.index_id] for i in results]

        if not results:
            results = []

        return results


class IndexPointAPI(ApiViewHandler):

    @login_required
    def get(self, index_id):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        df = SurfingQuery.get_index_point(
            index_id,
            start_date,
            end_date,
        )

        data = {
            'point': df['close'].to_list(),
            'dates': df['datetime'].to_list(),
        }

        return replace_nan(data)


class IndexMonthlyRetAPI(ApiViewHandler):

    @login_required
    def get(self, index_id):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        df = SurfingQuery.get_index_point(
            index_id,
            start_date,
            end_date,
            ('ret',),
        )
        df = df.set_index('datetime')
        returns = df['ret']

        ret = ep.aggregate_returns(returns, 'monthly')
        ret = pd.DataFrame(ret)
        ret.index = ['{}-{}'.format(index[0], index[1]) for index in ret.index]

        data = {
            'ret': ret['ret'].to_list(),
            'month': ret.index,
        }
        return replace_nan(data)
