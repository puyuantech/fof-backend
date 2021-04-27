
from flask import g

from bases.exceptions import LogicError
from bases.viewhandler import ApiViewHandler
from extensions.haifeng.fof_template import FOFTemplate
from models import InvestorInformation, RiskQuestion, RiskAnswer
from utils.decorators import login_required

from .constants import INVESTOR_CERTIFICATION_QUESTIONS
from .validators.information import (CertImageValidation, UserInfoValidation, RealNameValidation, RiskLevelValidation,
                                     ExperienceValidation, InfoTableValidation, CommitmentValidation)


class InformationAPI(ApiViewHandler):

    @login_required
    def get(self):
        return InvestorInformation.get_investor_information(g.token.investor_id)


class CertImageAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = CertImageValidation.get_valid_data(self.input)
        return InvestorInformation.update_investor_information(g.token.investor_id, **data)


class UserInfoAPI(ApiViewHandler):

    @login_required
    def get(self):
        return INVESTOR_CERTIFICATION_QUESTIONS

    @login_required
    def post(self):
        data = UserInfoValidation.get_valid_data(self.input)
        message = FOFTemplate().register_investor(g.token.investor_id, data)
        if message is not None:
            raise LogicError(message)
        return InvestorInformation.update_investor_information(g.token.investor_id, **data)


class RealNameAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = RealNameValidation.get_valid_data(self.input)
        data['real_name_image_url_key'] = data.pop('real_name_image')
        return InvestorInformation.update_investor_information(g.token.investor_id, **data)


class RiskLevelAPI(ApiViewHandler):

    @login_required
    def get(self):
        return [question.to_dict() for question in RiskQuestion.get_questions()]

    @login_required
    def post(self):
        data = RiskLevelValidation.get_valid_data(self.input)
        risk_level_score = RiskQuestion.calc_risk_score(data['risk_level_answers'])
        risk_level = RiskQuestion.get_risk_level_by_score(risk_level_score)

        RiskAnswer.create(
            investor_id=g.token.investor_id,
            risk_level_answers=data['risk_level_answers'],
            risk_level=risk_level,
            risk_level_score=risk_level_score,
        )

        return InvestorInformation.update_investor_information(
            investor_id=g.token.investor_id,
            risk_level=risk_level,
            risk_level_score=risk_level_score,
            **data
        )


class ExperienceAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ExperienceValidation.get_valid_data(self.input)
        return InvestorInformation.update_investor_information(g.token.investor_id, **data)


class InfoTableAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = InfoTableValidation.get_valid_data(self.input)
        data['info_table_url_key'] = data.pop('info_table')
        return InvestorInformation.update_investor_information(g.token.investor_id, **data)


class CommitmentAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = CommitmentValidation.get_valid_data(self.input)
        data['commitment_url_key'] = data.pop('commitment')
        return InvestorInformation.update_investor_information(g.token.investor_id, **data)

