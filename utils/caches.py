from bases.globals import cache


@cache.memoize(timeout=1800, make_name='get_fund_collection_caches')
def get_fund_collection_caches():
    import pandas as pd
    from surfing.data.wrapper.mysql import ViewDatabaseConnector
    from surfing.data.view.view_models import FundDailyCollection
    with ViewDatabaseConnector().managed_session() as mn_session:
        query = mn_session.query(
            FundDailyCollection.fund_id,
            FundDailyCollection.full_name,
            FundDailyCollection.order_book_id,
        )
        df = pd.read_sql(query.statement, query.session.bind)
        df = df.rename(columns={
            'full_name': 'fund_name'
        })
    return df.set_index('fund_id')


@cache.memoize(timeout=30, make_name='get_hedge_fund_cache')
def get_hedge_fund_cache():
    import pandas as pd
    from bases.globals import db
    from models import HedgeFundInfo

    results = db.session.query(
        HedgeFundInfo,
    ).all()
    df = pd.DataFrame([i.to_dict() for i in results])
    df['order_book_id'] = df['fund_id']
    return df.set_index('fund_id')


@cache.memoize(timeout=30, make_name='get_fund_cache')
def get_fund_cache():
    data = dict()
    mutual_fund = get_fund_collection_caches()
    hedge_fund = get_hedge_fund_cache()

    for i in mutual_fund.index:
        data[i] = mutual_fund.loc[i, 'fund_name']

    for i in hedge_fund.index:
        data[i] = hedge_fund.loc[i, 'fund_name']

    return data

