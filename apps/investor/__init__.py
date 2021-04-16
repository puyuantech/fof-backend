from flask import Blueprint
from flask_restful import Api

from .view_certification import (LatestAPI, EffectiveAPI, ApplyAPI, SubmitAPI,
                                 ApproveAPI, UnapproveAPI, ReapplyAPI)
from .view_content import ContentStatisticsAPI
from .view_contract import (ContractAPI, ContractListAPI, ContractTemplateAPI, RiskDiscloseAPI,
                            FundContractAPI, ProtocolAPI, FundMatchingAPI, VideoAPI, LookbackAPI,
                            BookAPI, SignAPI)
from .view_information import (InformationAPI, InvestorTokenAPI, FaceImageAPI, CertImageAPI,
                               RealNameAPI, RiskLevelAPI, ExperienceAPI, InfoTableAPI, CommitmentAPI)
from .view_notification import NotificationMenuAPI, NotificationListAPI, NotificationReadListAPI
from .view_position import PositionListAPI, PositionAnalysisAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/investor')
api = Api(blu)

api.add_resource(LatestAPI, '/certification/latest')
api.add_resource(EffectiveAPI, '/certification/effective')
api.add_resource(ApplyAPI, '/certification/apply')
api.add_resource(SubmitAPI, '/certification/submit')
api.add_resource(ApproveAPI, '/certification/approve')
api.add_resource(UnapproveAPI, '/certification/unapprove')
api.add_resource(ReapplyAPI, '/certification/reapply')

api.add_resource(ContentStatisticsAPI, '/content/statistics')

api.add_resource(ContractAPI, '/contract')
api.add_resource(ContractListAPI, '/contract/list')
api.add_resource(ContractTemplateAPI, '/contract/template')
api.add_resource(RiskDiscloseAPI, '/contract/risk_disclose')
api.add_resource(FundContractAPI, '/contract/fund_contract')
api.add_resource(ProtocolAPI, '/contract/protocol')
api.add_resource(FundMatchingAPI, '/contract/fund_matching')
api.add_resource(VideoAPI, '/contract/video')
api.add_resource(LookbackAPI, '/contract/lookback')
api.add_resource(BookAPI, '/contract/book')
api.add_resource(SignAPI, '/contract/sign')

api.add_resource(InformationAPI, '/information')
api.add_resource(InvestorTokenAPI, '/information/token')
api.add_resource(FaceImageAPI, '/information/face_image')
api.add_resource(CertImageAPI, '/information/cert_image')
api.add_resource(RealNameAPI, '/information/real_name')
api.add_resource(RiskLevelAPI, '/information/risk_level')
api.add_resource(ExperienceAPI, '/information/experience')
api.add_resource(InfoTableAPI, '/information/info_table')
api.add_resource(CommitmentAPI, '/information/commitment')

api.add_resource(NotificationMenuAPI, '/notification/menu')
api.add_resource(NotificationListAPI, '/notification/list')
api.add_resource(NotificationReadListAPI, '/notification/read/list')

api.add_resource(PositionListAPI, '/position/list')
api.add_resource(PositionAnalysisAPI, '/position/analysis')
