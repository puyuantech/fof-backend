import json
import datetime
from flask import request, g, current_app
from models import Operation, Token
from models import UnitMap, InvestorInfo, User, UserInvestorMap
from bases.globals import db


def user_operation_log_middleware(app):

    @app.after_request
    def after_request(response):

        # 记录投资者最后操作时间
        if hasattr(g, 'user') and hasattr(g, 'token'):
            user = g.user
            token = g.token
            if not user.is_staff:
                obj = db.session.query(UnitMap).filter(
                    UserInvestorMap.user_id == user.id,
                    InvestorInfo.investor_id == UserInvestorMap.investor_id,
                    UnitMap.investor_id == InvestorInfo.investor_id,
                    UnitMap.manager_id == token.manager_id,
                ).first()
                if obj:
                    obj.latest_time = datetime.datetime.now()
                    obj.save()

        if not hasattr(g, 'user_operation'):
            return response

        if not hasattr(g, 'user_operation_params'):
            user_operation_params = {}
        else:
            user_operation_params = g.user_operation_params

        if not hasattr(g, 'user'):
            g.user = User()
            g.user.id = 0

        if not hasattr(g, 'token'):
            g.token = Token()

        remote_addr = request.headers.get('X-Real-Ip') if request.headers.get('X-Real-Ip') else '0.0.0.0'

        try:
            Operation.create(
                user_id=g.user.id,
                investor_id=g.token.investor_id,
                manager_id=g.token.manager_id,
                ip=str(remote_addr),
                action=g.user_operation,
                url=str(request.url),
                method=request.method,
                request_data=json.dumps(user_operation_params),
                response_data='',
                response_status=response.status,
            )
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(response.data)

        return response
