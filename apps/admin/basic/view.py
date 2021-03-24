import hashlib
from flask import g, request, current_app, make_response
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import ManagerWeChatAccount
from utils.decorators import params_required, login_required


class WeChatSettingAPI(ApiViewHandler):

    @login_required
    def get(self, manager_id):
        ManagerWeChatAccount.filter_by_query(

        )
        return
