from apps.accounts import blu as accounts_blu
from apps.auth import blu as auth_blu
from apps.captchas import blu as captcha_blu
from apps.stuff import blu as stuff_blu
from apps.productions import blu as production_blu
from apps.hedge import blu as hedge_blu

routers = [
    auth_blu,
    accounts_blu,
    captcha_blu,
    stuff_blu,
    production_blu,
    hedge_blu,
]

