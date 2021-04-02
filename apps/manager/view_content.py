
from flask import g

from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required

from .libs import get_contents


class ContentListAPI(ApiViewHandler):

    @login_required
    def get(self):
        return get_contents(g.token.manager_id)

