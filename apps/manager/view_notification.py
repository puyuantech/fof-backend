
from bases.globals import db
from bases.viewhandler import ApiViewHandler
from models import FOFNotification
from utils.decorators import login_required

from .validators.notification import NotificationValidation


class NotificationAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = NotificationValidation.get_valid_data(self.input)
        for investor_id in data.pop('investor_ids'):
            FOFNotification(**data, investor_id=investor_id).save(commit=False)
        db.session.commit()
        return 'success'

