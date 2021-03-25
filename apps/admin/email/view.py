import traceback
import datetime
from flask import g, request

from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import ManagerEmailAccount
from utils.decorators import params_required, login_required
from extensions.mail.mail import Mail, Message


class MailVerifyAPI(ApiViewHandler):

    @params_required(*['verify_email', 'server', 'username', 'secret', 'port', 'is_ssl', 'sender'])
    @login_required
    def post(self):
        try:
            m = Mail(
                server=self.input.server,
                username=self.input.username,
                password=self.input.secret,
                port=self.input.port,
                use_ssl=self.input.is_ssl,
                default_sender=self.input.username,
            )
            msg = Message(
                '测试邮件',
                recipients=[self.input.verify_email],
                sender=(self.input.sender, self.input.username)
            )
            current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            msg.html = f'''
            <h3>测试成功</h3>
            <hr>
            <div>来自: FOF平台</div>
            <div>时间: {current_date}</div>
            '''
            m.send(msg)
        except Exception as e:
            print(request.json)
            print(traceback.format_exc())
            raise VerifyError('验证失败，请检查配置')
        return 'success'


class MailSettingAPI(ApiViewHandler):
    update_columns = [
        'server',
        'port',
        'is_ssl',
        'username',
        'secret',
        'sender',
    ]

    @login_required
    def get(self):
        obj = ManagerEmailAccount.filter_by_query(
            manager_id=g.token.manager_id,
        ).first()
        if not obj:
            return {}
        return obj.to_dict()

    @login_required
    def post(self):
        obj = ManagerEmailAccount.filter_by_query(
            manager_id=g.token.manager_id,
        ).first()
        if not obj:
            ManagerEmailAccount.create(
                manager_id=g.token.manager_id,
                server=request.json.get('server'),
                port=request.json.get('port'),
                is_ssl=request.json.get('is_ssl'),
                username=request.json.get('username'),
                secret=request.json.get('secret'),
                sender=request.json.get('sender'),
            )
            return 'success'
        for i in self.update_columns:
            if request.json.get(i) is not None:
                obj.update(commit=False, **{i: request.json.get(i)})
        obj.save()

    @login_required
    def delete(self):
        obj = ManagerEmailAccount.filter_by_query(
            manager_id=g.token.manager_id,
        ).first()
        if not obj:
            return {}
        obj.delete()
