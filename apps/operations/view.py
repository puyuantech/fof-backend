from flask import g
from bases.viewhandler import ApiViewHandler
from bases.view_mixin import ViewList
from models import Operation


class OperationsAPI(ApiViewHandler, ViewList):

    def get_objects(self):
        return Operation.filter_by_query(
            user_id=g.user.id
        )

