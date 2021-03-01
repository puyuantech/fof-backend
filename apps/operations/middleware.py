import json
from flask import request, g, current_app
from models import User, Operation


def user_operation_log_middleware(app):

    @app.after_request
    def after_request(response):

        if not hasattr(g, 'user_operation'):
            return response

        if g.user_operation.startswith('登录'):
            request_data = {}
            response_data = '{}'
        else:
            request_data = request.json
            response_data = request.data

        if not hasattr(g, 'user'):
            g.user = User()
            g.user.id = 0

        remote_addr = request.headers.get('X-Real-Ip') if request.headers.get('X-Real-Ip') else '0.0.0.0'

        try:
            Operation.create(
                user_id=g.user.id,
                ip=str(remote_addr),
                action=g.user_operation,
                url=str(request.url),
                method=request.method,
                request_data=json.dumps(request_data),
                response_data=json.dumps(json.loads(response_data)),
                response_status=response.status,
            )
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(request_data)
            current_app.logger.error(response.data)

        return response
