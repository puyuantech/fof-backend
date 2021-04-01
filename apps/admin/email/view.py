import traceback
import datetime
import imaplib
from flask import g, request

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import ManagerEmailAccount, ManagerNavEmail, FOFInfo
from utils.decorators import params_required, login_required
from extensions.mail.mail import Mail, Message


class EMAILTask(ApiViewHandler):
    TOKEN = 'jisn401f7ac837da42b97f613d789819f37bee6a'

    @params_required(*['verify_token'])
    def post(self):
        if self.TOKEN != self.input.verify_token:
            return

        results = db.session.query(
            FOFInfo.fof_id,
            FOFInfo.manager_id,
        ).filter(
            FOFInfo.is_deleted == False,
            FOFInfo.manager_id != '1',
            FOFInfo.asset_type == 'production',
        ).all()
        print(results)
        data = []
        for i in results:
            d = {
                'manager_id': i[1],
                'fof_id': i[0],
            }
            obj = ManagerNavEmail.filter_by_query(
                manager_id=i[1],
            ).first()
            print(obj)
            if obj:
                d.update(obj.to_dict())
                data.append(d)

        return data


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


class NavMailVerifyAPI(ApiViewHandler):

    @params_required(*['server', 'port', 'email', 'password'])
    @login_required
    def post(self):
        try:
            with imaplib.IMAP4_SSL(host=self.input.server, port=self.input.port) as M:
                M.login(self.input.email, self.input.password)
                M.select(mailbox='Inbox', readonly=True)
        except Exception as e:
            print(request.json)
            print(traceback.format_exc())
            raise VerifyError('验证失败，请检查配置')
        return 'success'


class NavMailSetting(ApiViewHandler):
    update_columns = [
        'server',
        'port',
        'email',
        'password',
    ]

    @login_required
    def get(self):
        obj = ManagerNavEmail.filter_by_query(
            manager_id=g.token.manager_id,
        ).first()
        if not obj:
            return {}
        return obj.to_dict()

    @login_required
    def post(self):
        obj = ManagerNavEmail.filter_by_query(
            manager_id=g.token.manager_id,
        ).first()
        if not obj:
            ManagerNavEmail.create(
                manager_id=g.token.manager_id,
                server=request.json.get('server'),
                port=request.json.get('port'),
                email=request.json.get('email'),
                password=request.json.get('password'),
            )
            return 'success'
        for i in self.update_columns:
            if request.json.get(i) is not None:
                obj.update(commit=False, **{i: request.json.get(i)})
        obj.save()

    @login_required
    def delete(self):
        obj = ManagerNavEmail.filter_by_query(
            manager_id=g.token.manager_id,
        ).first()
        if not obj:
            return {}
        obj.delete()
