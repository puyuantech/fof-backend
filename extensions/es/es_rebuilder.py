import pandas as pd
from extensions.es.es_builder import FOFFundSearchBuilder, FOFManagementSearchBuilder
from extensions.es.es_models import FOFFundSearchDoc, FOFManagementSearchDoc
from bases.globals import settings, db
from models import ManagementFund, Management
from apps import create_app
create_app().app_context().push()


def fof_fund_search_rebuilder():
    builder = FOFFundSearchBuilder(label='es_test', doc_model=FOFFundSearchDoc)
    builder.init_rebuild_index()

    query = db.session.query(ManagementFund)
    df = pd.read_sql(query.statement, query.session.bind)
    for index in df.index:
        param = builder.build_doc_param(
            df.loc[index, 'fund_no'],
            df.loc[index, 'fund_name'],
        )
        builder.add_bulk_data(df.loc[index, 'fund_no'], param)
    builder.done_rebuild_index()


def fof_management_search_rebuilder():
    builder = FOFManagementSearchBuilder(label='es_test', doc_model=FOFManagementSearchDoc)
    builder.init_rebuild_index()

    query = db.session.query(
        Management.register_no,
        Management.manager_name,
    )
    df = pd.read_sql(query.statement, query.session.bind)
    for index in df.index:
        param = builder.build_doc_param(
            df.loc[index, 'register_no'],
            df.loc[index, 'manager_name'],
        )
        builder.add_bulk_data(df.loc[index, 'register_no'], param)
    builder.done_rebuild_index()


def re_build():
    fof_fund_search_rebuilder()
    print('fof fund rebuilder done!')

    fof_management_search_rebuilder()
    print('fof management rebuilder done!')


if __name__ == '__main__':
    re_build()
