from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import ApplyFile
from utils.decorators import params_required
from utils.helper import generate_random_str
from apps.captchas.libs import check_sms_captcha


class AppliesAPI(ApiViewHandler):

    @params_required(*['email', 'manager_id', 'manager_name', 'mobile', 'code'])
    def post(self):
        if self.is_valid_password(self.input.email):
            raise VerifyError('邮箱格式不正确')

        check_sms_captcha(
            verification_code=self.input.code,
            verification_key=self.input.mobile,
        )

        sec = generate_random_str(30)
        obj = ApplyFile.create(
            rand_str=sec,
            email=self.input.email,
            mobile=self.input.mobile,
            manager_name=self.input.manager_name,
            manager_id=self.input.manager_id,
        )
        return {
            'rand_str': obj.rand_str,
            'email': obj.email,
            'mobile': obj.mobile,
            'manager_name': obj.manager_name,
            'manager_id': obj.manager_id,
            'id': obj.id,
        }

    @params_required(*[
        'id',
        'rand_str',
        'manager_cred_type',
        'manager_cred_file',
        'manager_cred_no',
        'legal_person',
        'lp_cred_type',
        'lp_cred_file',
        'lp_cred_no',
        'authorization_file',
        'admin_name',
        'admin_cred_no',
    ])
    def put(self):
        obj = ApplyFile.get_by_query(
            id=self.input.id,
            rand_str=self.input.rand_str,
        )
        obj.manager_cred_type = self.input.manager_cred_type
        obj.manager_cred_file = self.input.manager_cred_file
        obj.manager_cred_no = self.input.manager_cred_no
        obj.legal_person = self.input.legal_person
        obj.lp_cred_type = self.input.lp_cred_type
        obj.lp_cred_file = self.input.lp_cred_file
        obj.lp_cred_no = self.input.lp_cred_no
        obj.authorization_file = self.input.authorization_file
        obj.admin_name = self.input.admin_name
        obj.admin_cred_no = self.input.admin_cred_no

        obj.save()
        return 'success'
