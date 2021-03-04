import traceback
from flask import views, request, jsonify, make_response, current_app, abort, g, Response
from .basehandler import BaseHandler, Dict
from .exceptions import AuthError, LogicError, ParamsError, VerifyError, BaseError


class BaseViewHandler(views.MethodView, BaseHandler):

    @property
    def input(self):
        d = Dict(request.values.items())
        if request.is_json:
            d.update(request.json)
        return d


class ApiViewHandler(BaseViewHandler):
    auth = None

    def dispatch_request(self, *args, **kwargs):
        self.set_header = {}
        self.set_cookie = {}
        self.delete_cookie = []
        self.http_origin = request.environ.get('HTTP_ORIGIN', '')

        handler = getattr(self, request.method.lower(), None)

        if not callable(handler):
            if request.method == 'HEAD':
                return make_response('', 200)
            else:
                abort(405)

        return self.api_wrapper(handler, *args, **kwargs)

    def api_wrapper(self, handler, *args, **kwargs):
        code = 1000
        data = msg = None
        status_code = 200
        start_time = self.get_timestamp()
        try:
            data = handler(*args, **kwargs)
        except AuthError as e:
            code = e.code
            status_code = e.status
            msg = str(e)
        except LogicError as e:
            code = e.code
            msg = str(e)
            status_code = e.status
            err = traceback.format_exc()
            current_app.logger.error(err)
        except ParamsError as e:
            code = e.code
            msg = str(e)
            status_code = e.status
        except VerifyError as e:
            code = e.code
            msg = str(e)
            status_code = e.status
        except BaseError as e:
            code = e.code
            msg = str(e)
            status_code = e.status
            err = traceback.format_exc()
            current_app.logger.error(err)
        except Exception:
            code = 5000
            msg = '内部错误'
            status_code = 500
            err = traceback.format_exc()
            current_app.logger.error(err)

        if isinstance(data, Response):
            return data

        cost_time = self.get_timestamp() - start_time

        res = {'code': code, 'data': data, 'cost': "{0}ms".format(round(cost_time * 1000, 2))}

        if msg:
            res.update({'msg': msg})

        try:
            response = make_response(jsonify(res), status_code)
        except Exception:
            print(traceback.format_exc())
            response = make_response(jsonify({'data': '解码错误！'}), 500)

        if self.set_header:
            for k, v in self.set_header.items():
                response.headers[k] = v

        if self.set_cookie:
            for k, v in self.set_cookie.items():
                response.set_cookie(k, v)

        if self.delete_cookie:
            for k in self.delete_cookie:
                response.delete_cookie(k)

        return response

