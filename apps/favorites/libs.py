from models import HedgeFundInfo


def make_hedge_favorite_info(obj):
    data = obj.to_dict()
    funds = HedgeFundInfo.filter_by_query(fund_id=obj.fund_id, show_deleted=True).all()
    if len(funds) > 0:
        fund = funds[0]
        fund = fund.to_dict(remove_deleted=False)
        fund['favorite_status'] = True

        data.update({
            'fund': fund,
        })
        return data
    return data

