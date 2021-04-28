from flask import g, request
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan
from utils.caches import get_hedge_fund_cache
from surfing.data.api.raw import RawDataApi


class FOFHasNav(ApiViewHandler):

    @login_required
    def get(self):
        """有净值的私募基金"""
        df = RawDataApi().get_exsited_nav_hf_fund_list()
        return replace_nan(df.to_dict(orient='list'))


class FOFForHedge(ApiViewHandler):

    @login_required
    def get(self):
        """可添加为底层资产的私募"""
        exclude_ids = request.args.get('exclude_ids')
        if exclude_ids:
            exclude_ids = exclude_ids.split(',')

        df = get_hedge_fund_cache()
        df = df[df['manager_id'] == g.token.manager_id]
        df = df.reset_index()
        df = df[['fof_id', 'desc_name']]
        df = df[~df['fof_id'].isin(exclude_ids)]
        return replace_nan(df.to_dict(orient='list'))
