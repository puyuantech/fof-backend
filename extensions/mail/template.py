import datetime
from extensions.mail import Mail, Message


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
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M%S')
    msg.html = f'''<h4 style="text-align:center">{pro_name}</h4>
        <br>
        <div>单位净值: <span style="color: black;font-size:120%;font-weight:bold;">{nav}</span></div>
        <br>
        <div>累计净值: <span style="color: black;font-size:120%;font-weight:bold;">{acc_nav}</span></div>
        <br>
        <div>估值日期: <span style="color: black;font-size:120%;font-weight:bold;">{date}</span></div>
        <br>
        <hr>
        <div>来自: {sender} </div>
        <div>时间: {current_date} </div>
        '''
    m.send(msg)
    return True
