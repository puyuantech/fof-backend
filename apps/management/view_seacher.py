
from flask import request

from extensions.es.es_searcher import FOFFundSearcher, FOFManagementSearcher
from extensions.es.es_conn import ElasticSearchConnector
from extensions.es.es_models import FOFFundSearchDoc, FOFManagementSearchDoc
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required


class FOFFundSearcherAPI(ApiViewHandler):

    @login_required
    def get(self, key_word):
        page = int(request.args.get('page', 0))
        page_size = int(request.args.get('page_size', 5))
        offset = page * page_size

        conn = ElasticSearchConnector().get_conn()
        searcher = FOFFundSearcher(conn, key_word, FOFFundSearchDoc)
        results, count = searcher.get_usually_query_result(key_word, offset, page_size)
        results = [[i.fof_id, i.fof_name] for i in results]

        if not results:
            results = []

        return results


class FOFManagementSearcherAPI(ApiViewHandler):

    @login_required
    def get(self, key_word):
        page = int(request.args.get('page', 0))
        page_size = int(request.args.get('page_size', 5))
        offset = page * page_size

        conn = ElasticSearchConnector().get_conn()
        searcher = FOFManagementSearcher(conn, key_word, FOFManagementSearchDoc)
        results, count = searcher.get_usually_query_result(key_word, offset, page_size)
        results = [[i.management_id, i.management_name] for i in results]

        if not results:
            results = []

        return results
