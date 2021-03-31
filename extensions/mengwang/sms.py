import requests
import datetime
import json
from urllib import parse
import hashlib
from bases.globals import settings
from .templates import *


class MWMassage:

    def __init__(self):
        self.username = settings['SMS_MW'].get('username')
        self.password = settings['SMS_MW'].get('password')
        self.host = settings['SMS_MW'].get('host')
        self.port = settings['SMS_MW'].get('port')
        self.pwd = hashlib.md5('{}{}{}{}'.format(
            self.username,
            '00000000',
            self.password,
            datetime.datetime.now().strftime('%m%d%H%M%S'),
        ).encode()).hexdigest()

    def send_post(self, url: str, data: dict):
        headers = {
            'Content-Type': 'application/json'
        }
        return requests.post(
            url=url,
            data=json.dumps(data),
            headers=headers,
        )

    def single_send(self, mobile, content, svr_type='SMS001', ex_no='0006', customer_id='', ex_data=''):
        """
        此接口只最多并发100（文档说明）
        """
        url = f'http://{self.host}:{self.port}/sms/v2/std/single_send'
        content = content.encode('GBK')
        content = parse.quote(content)

        response = self.send_post(url, data={
            'userid': self.username,
            'pwd': self.pwd,
            'mobile': mobile,
            'content': content,
            'timestamp': datetime.datetime.now().strftime('%m%d%H%M%S'),
            'svrtype': svr_type,
            'exno': ex_no,
            'custid': customer_id,
            'exdata': ex_data,
        })
        return response

    def check_status(self, ):
        url = f'http://{self.host}:{self.port}/sms/v2/std/get_rpt'
        response = self.send_post(url, data={
            'userid': self.username,
            'pwd': self.pwd,
            'timestamp': datetime.datetime.now().strftime('%m%d%H%M%S'),
            'retsize': 10
        })
        return response


def sms_nav_template(send_to, pro_name, nav, acc_nav, date):
    cli = MWMassage()
    cli.single_send(
        send_to,
        TEMPLATE_PRODUCTION_NAV.format(
            pro_name,
            nav,
            acc_nav,
            date,
        )
    )


if __name__ == '__main__':
    c = MWMassage()
    template_1 = """尊敬的用户，您于{}的操作已{}，请进入微信小程序“棱镜智投tamp”通知中心查看详情。"""
    template_2 = """尊敬的用户，您在{}进行了调整，请登录微信小程序“棱镜智投tamp”确认。"""
    # res = c.single_send(
    #     '17610391011',
    #     template_1.format(
    #         '2019年12月01日15点08分申购<华夏幸福>',
    #         '成功',
    #     )
    # )
    # print(res.status_code)
    # res = c.single_send(
    #     '17610391011',
    #     template_2.format(
    #         '小站投资者之家订阅的组合<稳稳的幸福>',
    #         # '成功',
    #     )
    # )
    # res = c.single_send(
    #     '17610391011',
    #     """验证码：{}，您正在绑定账户手机号，请妥善保管验证码。""".format('009098')
    # )
    res = c.single_send(
        '17610391011',
        """尊敬的客户您好，您的基金产品净值已更新:
产品名称：{}
单位净值：{}
累计净值：{}
估值日期：{}""".format('1', '1', '1', '1')
    )
    print(res.status_code)
    print(res.text)
    res = c.check_status()
    print(res.text)



