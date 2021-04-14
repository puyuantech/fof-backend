
from flask import request

from extensions.es.es_searcher import FundSearcher
from extensions.es.es_conn import ElasticSearchConnector
from extensions.es.es_models import FundSearchDoc
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required


class FundSearcherAPI(ApiViewHandler):

    @login_required
    def get(self, key_word):
        page = int(request.args.get('page', 0))
        page_size = int(request.args.get('page_size', 5))
        offset = page * page_size

        conn = ElasticSearchConnector().get_conn()
        searcher = FundSearcher(conn, key_word, FundSearchDoc)
        results, count = searcher.get_usually_query_result(key_word, offset, page_size)
        results = [[i.order_book_id, i.desc_name, i.fund_id] for i in results]

        if not results:
            results = []

        return results
