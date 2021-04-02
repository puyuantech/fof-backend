from elasticsearch_dsl import Document, Date, Text, Keyword


class IndexSearchDoc(Document):

    index_id = Keyword()
    order_book_id = Text(analyzer='ik_max_word')
    desc_name = Text(analyzer='ik_max_word')
    desc_name_pinyin = Text(analyzer='pinyin')
    desc_name_first = Text(analyzer='standard')
    update_time = Date()
    create_time = Date()

    class Index:
        name = 'index_search'
        label_name = 'es_test'


class FOFFundSearchDoc(Document):

    fof_id = Keyword()
    fof_name = Text(analyzer='ik_max_word')
    fof_name_pinyin = Text(analyzer='pinyin')
    fof_name_first = Text(analyzer='standard')
    update_time = Date()
    create_time = Date()

    class Index:
        name = 'fof_fund_search'
        label_name = 'es_test'
