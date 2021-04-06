
from flask import g
from bases.viewhandler import ApiViewHandler
from models import InvestorCertification
from utils.decorators import login_required

from .validators.certification import UnitValidation, ApproveValidation, UnapproveValidation


class LatestAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = UnitValidation.get_valid_data(self.input)
        return InvestorCertification.get_latest_certification(**data)


class EffectiveAPI(ApiViewHandler):

    @login_required
    def get(self):
        data = UnitValidation.get_valid_data(self.input)
        return InvestorCertification.get_effective_certification(**data)


class ApplyAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = UnitValidation.get_valid_data(self.input)
        return InvestorCertification.apply_certification(**data)


class SubmitAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = UnitValidation.get_valid_data(self.input)
        return InvestorCertification.submit_certification(**data)


class ApproveAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ApproveValidation.get_valid_data(self.input)
        g.user_operation = '审核通过'
        g.user_operation_params = {
            'investor_id': data.get('investor_id'),
        }
        return InvestorCertification.approve_certification(**data)


class UnapproveAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = UnapproveValidation.get_valid_data(self.input)
        g.user_operation = '审核拒绝'
        g.user_operation_params = {
            'investor_id': data.get('investor_id'),
        }
        return InvestorCertification.unapprove_certification(**data)


class ReapplyAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = UnitValidation.get_valid_data(self.input)
        return InvestorCertification.reapply_certification(**data)

