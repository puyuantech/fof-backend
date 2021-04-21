from flask import Blueprint
from flask_restful import Api
from .view import *

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/manager_trades')
api = Api(blu)

api.add_resource(TradesDivCarAPI, '/div_car')
api.add_resource(TradesPurRedAPI, '/pur_redeem')
