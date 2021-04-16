from bases.exceptions import VerifyError
from bases.viewhandler import ApiViewHandler
from bases.globals import db
from models import UserInvestorMap, User, InvestorInfo
from utils.decorators import login_required, params_required


class SubAccount(ApiViewHandler):

    @login_required
    def get(self, investor_id):
        investor_info = InvestorInfo.filter_by_query(
            investor_id=investor_id
        ).first()
        if not investor_info:
            raise VerifyError('投资者账户不存在！')

        results = db.session.query(
            User.id,
            User.mobile,
            UserInvestorMap.map_type,
        ).filter(
            UserInvestorMap.is_deleted == False,
            UserInvestorMap.investor_id == investor_id,
            UserInvestorMap.user_id == User.id,
        ).all()
        return [{
            'user_id': i[0],
            'mobile': i[1],
            'map_type': i[2],
        } for i in results]

    @params_required(*['mobile'])
    @login_required
    def post(self, investor_id):
        if not self.is_valid_mobile(self.input.mobile):
            raise VerifyError('手机号码输入错误！')
        investor_info = InvestorInfo.filter_by_query(
            investor_id=investor_id
        ).first()
        if not investor_info:
            raise VerifyError('投资者账户不存在！')

        user = User.filter_by_query(
            mobile=self.input.mobile
        ).first()
        if not user:
            user, main_investor = User.create_main_user_investor(mobile=self.input.mobile)

        ui_map = UserInvestorMap.filter_by_query(
            investor_id=investor_id,
            user_id=user.id,
        ).first()
        if not ui_map:
            User.create_investor_sub_user(user.id, investor_id)
        user.last_login_investor = investor_id
        user.save()

        return 'success'

    @params_required(*['mobile'])
    @login_required
    def delete(self, investor_id):
        if not self.is_valid_mobile(self.input.mobile):
            raise VerifyError('手机号码输入错误！')
        investor_info = InvestorInfo.filter_by_query(
            investor_id=investor_id
        ).first()
        if not investor_info:
            raise VerifyError('投资者账户不存在！')

        user = User.filter_by_query(
            mobile=self.input.mobile
        ).first()
        if not user:
            raise VerifyError('手机号不存在账户')

        ui_map = UserInvestorMap.filter_by_query(
            investor_id=investor_id,
            user_id=user.id,
        ).first()
        if not ui_map:
            return
        ui_map.logic_delete()
        return 'success'
