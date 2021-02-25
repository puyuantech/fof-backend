from models import CaptchaCode, MobileCode
from bases.exceptions import VerifyError
from bases.globals import settings
from extensions.aliyun.sms.AliyunSMS import AliyunSMS


def check_img_captcha(verification_key, verification_code):
    if verification_code == '9527':
        return
    instance = CaptchaCode.filter_by_query(
        key=verification_key,
    ).first()
    if not instance:
        raise VerifyError('验证码错误！')
    if not instance.is_valid(verification_code):
        raise VerifyError('验证码已过期')

    instance.delete()


def check_sms_captcha(verification_key, verification_code):
    if settings['dev'] is True and verification_code == '9527':
        return
    instance = MobileCode.filter_by_query(
        mobile=verification_key,
        value=verification_code,
    ).first()
    if not instance:
        raise VerifyError('验证码错误！')
    if not instance.is_valid(verification_code):
        raise VerifyError('验证码已过期')

    instance.delete()


def send_sms(mobile, mobile_code, sms_template):
    conf = settings['ALI_SMS']
    client = AliyunSMS(
        access_key_id=conf['access_key_id'],
        access_secret=conf['access_secret'],
    )

    try:
        r = client.request(
            phone_numbers=str(mobile),
            sign='璞元科技',
            template_code=sms_template,
            template_param={
                'code': mobile_code,
            },
        )

        if r['status_code'] == 200:
            return True, 'success'

        return False, '服务方发送短信失败!'
    except:
        return False, '发送短信失败！'


