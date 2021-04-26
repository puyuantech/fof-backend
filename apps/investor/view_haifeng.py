
from bases.viewhandler import ApiViewHandler
from extensions.haifeng.haifeng_token import HaiFengToken
from utils.decorators import login_required


class HaiFengTokenAPI(ApiViewHandler):

    @login_required
    def get(self):
        return HaiFengToken().get_token()


class HaiFengHeadersAPI(ApiViewHandler):

    @login_required
    def get(self):
        return HaiFengToken().get_headers()

