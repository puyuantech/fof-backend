import re
from elasticsearch import NotFoundError
from elasticsearch_dsl.query import Match, MatchPhrasePrefix, Regexp
from elasticsearch_dsl import Q


class Searcher:

    def __init__(self, conn, filters, doc_model):
        self.conn = conn
        self.filters = filters
        self.doc_model = doc_model

    def search_by_id(self, id):
        if self.doc_model is None:
            raise Exception('no doc model found')
        try:
            return self.doc_model.get(id)
        except NotFoundError as ex:
            return None
        except Exception as e:
            raise e

    def get_usually_query_result(self, key_word, offset, limit):
        return [], 0


class IndexSearcher(Searcher):

    def get_usually_query_result(self, key_word, offset, limit):
        must, must_not, should, filters = [], [], [], []
        ss = self.doc_model.search()
        zh_model = re.compile(u'[a-z]')

        if key_word.isdigit():
            should.append(Regexp(order_book_id='.*{}'.format(key_word)))
            should.append(Regexp(order_book_id='.*{}.*'.format(key_word)))
            # should.append(MatchPhrasePrefix(order_book_id=key_word))
        elif zh_model.search(key_word):
            should.append(MatchPhrasePrefix(desc_name_pinyin=key_word))
            should.append(MatchPhrasePrefix(desc_name_first=key_word))
        else:
            should.append(Match(desc_name=key_word))

        should_match = 1  # if should else 0
        s = ss.query(Q(
            'bool',
            must=must,
            filter=filters,
            must_not=must_not,
            should=should,
            minimum_should_match=should_match
        ))

        _ = s[offset: offset + limit].execute()
        count = _.hits.total
        return _.hits, count


class FOFFundSearcher(Searcher):

    def get_usually_query_result(self, key_word, offset, limit):
        must, must_not, should, filters = [], [], [], []
        ss = self.doc_model.search()
        zh_model = re.compile(u'[a-z]')

        if re.compile(u'[0-9]').search(key_word):
            should.append(Regexp(fof_id='.*{}'.format(key_word)))
            should.append(Regexp(fof_id='.*{}.*'.format(key_word)))
        elif zh_model.search(key_word):
            should.append(MatchPhrasePrefix(fof_name_pinyin=key_word))
            should.append(MatchPhrasePrefix(fof_name_first=key_word))
        else:
            should.append(Match(fof_name=key_word))

        should_match = 1  # if should else 0
        s = ss.query(Q(
            'bool',
            must=must,
            filter=filters,
            must_not=must_not,
            should=should,
            minimum_should_match=should_match
        ))

        _ = s[offset: offset + limit].execute()
        count = _.hits.total
        return _.hits, count


class FundSearcher(Searcher):

    def get_usually_query_result(self, key_word, offset, limit):
        must, must_not, should, filters = [], [], [], []
        ss = self.doc_model.search()
        zh_model = re.compile(u'[a-z]')

        if key_word.isdigit():
            should.append(Regexp(order_book_id='.*{}'.format(key_word)))
            should.append(Regexp(order_book_id='.*{}.*'.format(key_word)))
        elif zh_model.search(key_word):
            should.append(MatchPhrasePrefix(desc_name_pinyin=key_word))
            should.append(MatchPhrasePrefix(manager_name_pinyin=key_word))
            should.append(MatchPhrasePrefix(desc_name_first=key_word))
            should.append(MatchPhrasePrefix(manager_name_first=key_word))
        else:
            should.append(Match(desc_name=key_word))
            should.append(Match(manager_name=key_word))

        should_match = 1  # if should else 0
        s = ss.query(Q(
            'bool',
            must=must,
            filter=filters,
            must_not=must_not,
            should=should,
            minimum_should_match=should_match
        ))

        _ = s[offset: offset + limit].execute()
        count = _.hits.total
        return _.hits, count


class FOFManagementSearcher(Searcher):

    def get_usually_query_result(self, key_word, offset, limit):
        must, must_not, should, filters = [], [], [], []
        ss = self.doc_model.search()
        zh_model = re.compile(u'[a-z]')

        if re.compile(u'[0-9]').search(key_word):
            should.append(Regexp(management_id='.*{}'.format(key_word)))
            should.append(Regexp(management_id='.*{}.*'.format(key_word)))
        elif zh_model.search(key_word):
            should.append(MatchPhrasePrefix(management_name_pinyin=key_word))
            should.append(MatchPhrasePrefix(management_name_first=key_word))
        else:
            should.append(Match(management_name=key_word))

        should_match = 1  # if should else 0
        s = ss.query(Q(
            'bool',
            must=must,
            filter=filters,
            must_not=must_not,
            should=should,
            minimum_should_match=should_match
        ))

        _ = s[offset: offset + limit].execute()
        count = _.hits.total
        return _.hits, count