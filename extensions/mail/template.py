import datetime
from extensions.mail import Mail, Message


def mail_captcha_code(server, username, password, port, use_ssl, sender, title, send_to, code):
    m = Mail(
        server=server,
        username=username,
        password=password,
        port=port,
        use_ssl=use_ssl,
        default_sender=username,
    )
    msg = Message(
        title,
        recipients=[send_to],
        sender=(sender, username)
    )
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg.html = f'''
        <div>尊敬的用户您好:</div>
        <br>
        <div>您的验证码为: <span style="color: #173177;font-size:120%;font-weight:bold;">{code}</span> 请妥善保管</div>
        <br>
        <hr>
        <div>来自: {sender} </div>
        <div>时间: {current_date} </div>
        '''
    m.send(msg)
    return True


def mail_nav_template(server, username, password, port, use_ssl, sender, title, send_to, pro_name, nav, acc_nav, date):
    m = Mail(
        server=server,
        username=username,
        password=password,
        port=port,
        use_ssl=use_ssl,
        default_sender=username,
    )
    msg = Message(
        title,
        recipients=[send_to],
        sender=(sender, username)
    )
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg.html = f'''
        <div>产品名称: <span style="color: black;font-size:120%;font-weight:bold;">{pro_name}</span></div>
        <br>
        <div>单位净值: <span style="color: #173177;font-size:120%;font-weight:bold;">{nav}</span></div>
        <br>
        <div>累计净值: <span style="color: #173177;font-size:120%;font-weight:bold;">{acc_nav}</span></div>
        <br>
        <div>估值日期: <span style="color: black;font-size:100%;font-weight:bold;">{date}</span></div>
        <br>
        <hr>
        <div>来自: {sender} </div>
        <div>时间: {current_date} </div>
        '''
    m.send(msg)
    return True


def mail_admin_failed_sign_template(server, username, password, port, use_ssl, sender, title, send_to, name, err_msg):
    m = Mail(
        server=server,
        username=username,
        password=password,
        port=port,
        use_ssl=use_ssl,
        default_sender=username,
    )
    msg = Message(
        title,
        recipients=[send_to],
        sender=(sender, username)
    )
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg.html = f'''
        <div>尊敬的用户您好:</div>
        <br>
        <div>您入驻申请: <span style="color: #173177;font-size:120%;font-weight:bold;">{name}</span></div>
        <div>审核未通过: <span style="color: #173177;font-size:120%;font-weight:bold;">{err_msg}</span></div>
        <br>
        <hr>
        <div>来自: {sender} </div>
        <div>时间: {current_date} </div>
        '''
    m.send(msg)
    return True


def mail_admin_success_sign_template(server, username, password, port, use_ssl, sender, title, send_to, name, admin_name, admin_sec):
    m = Mail(
        server=server,
        username=username,
        password=password,
        port=port,
        use_ssl=use_ssl,
        default_sender=username,
    )
    msg = Message(
        title,
        recipients=[send_to],
        sender=(sender, username)
    )
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg.html = f'''
        <div>尊敬的用户您好:</div>
        <br>
        <div>您入驻申请: <span style="color: #173177;font-size:120%;font-weight:bold;">{name}</span> 已通过</div>
        <br>
        <div>管理员账号: <span style="color: #173177;font-size:120%;font-weight:bold;">{admin_name}</span></div>
        <br>
        <div>管理员密码: <span style="color: #173177;font-size:120%;font-weight:bold;">{admin_sec}</span></div>
        <br>
        <div>请登陆后尽快修改管理员密码</div>
        <hr>
        <div>来自: {sender} </div>
        <div>时间: {current_date} </div>
        '''
    m.send(msg)
    return True


if __name__ == '__main__':

    from bases.globals import settings
    print(settings)

    mail_admin_failed_sign_template(
        settings['MAIL_SERVER'],
        settings['MAIL_EMAIL'],
        settings['MAIL_PASSWORD'],
        settings['MAIL_PORT'],
        settings['MAIL_SSL'],
        settings['MAIL_SENDER'],
        '入驻提醒',
        'wj@puyuan.tech',
        '棱镜测试',
        '未知错误',
    )
    mail_admin_success_sign_template(
        settings['MAIL_SERVER'],
        settings['MAIL_EMAIL'],
        settings['MAIL_PASSWORD'],
        settings['MAIL_PORT'],
        settings['MAIL_SSL'],
        settings['MAIL_SENDER'],
        '入驻提醒',
        'wj@puyuan.tech',
        '棱镜测试',
        'username',
        'password'
    )

