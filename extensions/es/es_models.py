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


class FundSearchDoc(Document):

    fund_id = Keyword()
    order_book_id = Text(analyzer='ik_max_word')
    desc_name = Text(analyzer='ik_max_word')
    desc_name_pinyin = Text(analyzer='pinyin')
    desc_name_first = Text(analyzer='standard')
    manager_name = Text(analyzer='ik_max_word')
    manager_name_pinyin = Text(analyzer='pinyin')
    manager_name_first = Text(analyzer='standard')
    update_time = Date()
    create_time = Date()

    class Index:
        name = 'fund_search'
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


class FOFManagementSearchDoc(Document):

    management_id = Keyword()
    management_name = Text(analyzer='ik_max_word')
    management_name_pinyin = Text(analyzer='pinyin')
    management_name_first = Text(analyzer='standard')
    update_time = Date()
    create_time = Date()

    class Index:
        name = 'fof_management_search'
        label_name = 'es_test'
