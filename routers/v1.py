from apps.accounts import blu as accounts_blu
from apps.auth import blu as auth_blu
from apps.captchas import blu as captcha_blu
from apps.stuff import blu as stuff_blu
from apps.productions import blu as production_blu
from apps.hedge import blu as hedge_blu
from apps.customers import blu as customer_blu
from apps.markets import blu as market_blu
from apps.logic import blu as logic_blu
from apps.wx import blu as wx_blu
from apps.favorites import blu as favorite_blu
from apps.allocations import blu as allocation_blu
from apps.operations import blu as operation_blu
from apps.index import blu as index_blu
from apps.informations import blu as info_blu
from apps.uploads import blu as upload_blu

routers = [
    auth_blu,
    accounts_blu,
    captcha_blu,
    stuff_blu,
    production_blu,
    hedge_blu,
    customer_blu,
    market_blu,
    logic_blu,
    wx_blu,
    favorite_blu,
    allocation_blu,
    operation_blu,
    index_blu,
    info_blu,
    upload_blu,
]
