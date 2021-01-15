import uuid
import base64
import random

from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError, LogicError
from utils.decorators import params_required
from models import CaptchaCode, MobileCode, User
from bases.constants import SMS

from .captcha import captcha
from .captcha import utils
from .captcha.settings import DEFAULTS
from .libs import check_img_captcha, send_sms


class GetCaptcha(ApiViewHandler):
    def get(self):
        key = str(uuid.uuid4())
        code = utils.random_char_challenge(DEFAULTS.CAPTCHA_LENGTH)

        # generate image
        image_bytes = captcha.generate_image(code)
        image_b64 = base64.b64encode(image_bytes)
        print(key, code)
        data = {
            DEFAULTS.CAPTCHA_KEY: key,
            DEFAULTS.CAPTCHA_IMAGE: image_b64.decode(),
            'image_type': 'image/png',
            'image_decode': 'base64'
        }
        CaptchaCode.create(
            key=key,
            value=code,
            expires_at=CaptchaCode.generate_expires_at()
        )
        return data


class CaptchaCheckAPI(ApiViewHandler):
    @params_required(*['verification_code', 'verification_key'])
    def post(self):
        check_img_captcha(
            verification_code=self.input.verification_code,
            verification_key=self.input.verification_key,
        )


class GetMobileCaptcha(ApiViewHandler):
    @params_required(*['mobile', 'action'])
    def post(self):
        if not self.is_valid_mobile(self.input.mobile):
            raise VerifyError('手机号输入错误！')

        User.get_by_query(mobile=self.input.mobile)
        mobile = self.input.mobile
        code = '%(code)06d' % {
            'code': random.randint(1, 999999),
        }
        if self.input.action == 'login':
            print(mobile, code)
            action = SMS.LOGIN
            status, msg = send_sms(mobile, code, action)
            if not status:
                raise LogicError(msg)
        else:
            raise VerifyError('非正确途径')

        MobileCode.create(
            mobile=mobile,
            value=code,
            action=action,
            expires_at=MobileCode.generate_expires_at(),
        )
        return

