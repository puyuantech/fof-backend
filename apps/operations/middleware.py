import json
from flask import request, g, current_app
from models import User, Operation, Token


def user_operation_log_middleware(app):

    @app.after_request
    def after_request(response):

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
