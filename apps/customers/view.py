import pandas as pd
import io
import datetime
from flask import request, g, views, make_response

from models import User, UserLogin, FOFInvestorPosition, FOFScaleAlteration, FOFInfo
from bases.globals import db
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from bases.constants import StuffEnum
from utils.helper import generate_sql_pagination, replace_nan
from utils.decorators import params_required, super_admin_login_required, admin_login_required, login_required
from utils.caches import get_fund_collection_caches, get_hedge_fund_cache
from .libs import get_all_user_info_by_user, register_investor_user, update_user_info, update_trade, parse_trade_file, \
    create_single_trade


class CusAPI(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def get(self):
        p = generate_sql_pagination()
        query = User.filter_by_query(role_id=StuffEnum.INVESTOR)
        data = p.paginate(query, call_back=lambda x: [get_all_user_info_by_user(i) for i in x])
        return data

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    @params_required(*['mobile', 'investor_id'])
    def post(self):
        if not self.is_valid_mobile(self.input.mobile):
            raise VerifyError('电话号码有误！')

        if User.filter_by_query(investor_id=self.input.investor_id).first():
            raise VerifyError('投资者ID已存在')

        # 创建投资者
        user, user_login = register_investor_user(
            self.input.mobile,
        )

        # 添加信息
        update_user_info(user)
        return 'success'


class CustomerAPI(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def get(self, _id):
        instance = User.filter_by_query(id=_id, role_id=StuffEnum.INVESTOR).first()
        if not instance:
            raise VerifyError('不存在！')
        return get_all_user_info_by_user(instance)

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def put(self, _id):
        instance = User.filter_by_query(id=_id, role_id=StuffEnum.INVESTOR).first()
        if not instance:
            raise VerifyError('不存在！')
        user = update_user_info(instance)
        return get_all_user_info_by_user(user)

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def delete(self, _id):
        user = User.filter_by_query(id=_id, role_id=StuffEnum.INVESTOR).first()
        if not user:
            raise VerifyError('不存在！')
        user_login = UserLogin.filter_by_query(user_id=user.id).first()
        if user_login:
            user_login.delete()
        user.logic_delete()


class CustomerPosition(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def get(self, investor_id):

        results = db.session.query(FOFInvestorPosition, FOFInfo.fof_name).filter(
            FOFInvestorPosition.investor_id == investor_id,
            FOFInfo.fof_id == FOFInvestorPosition.fof_id,
        ).all()

        df_data = []
        for i in results:
            d = i[0].to_dict()
            d['fof_name'] = i[1]
            df_data.append(d)

        df = pd.DataFrame(df_data)

        if len(df) < 1:
            return []

        df['sum_amount'] = df['amount'].sum()
        df['weight'] = df['amount'] / df['sum_amount']
        return replace_nan(df.to_dict(orient='records'))


class CustomerTrades(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def get(self, investor_id):
        results = db.session.query(FOFScaleAlteration, FOFInfo.fof_name).filter(
            FOFScaleAlteration.investor_id == investor_id,
            FOFInfo.fof_id == FOFScaleAlteration.fof_id,
        )
        df_list = []
        for i in results:
            d = i[0].to_dict()
            d['fof_name'] = i[1]
            df_list.append(d)

        df = pd.DataFrame(df_list)
        return replace_nan(df.to_dict(orient='records'))

    @login_required
    def put(self, investor_id):
        df = parse_trade_file(investor_id)

        for d in df.to_dict(orient='records'):
            new = FOFScaleAlteration(**replace_nan(d))
            db.session.add(new)
        db.session.commit()

    @login_required
    def post(self, investor_id):
        create_single_trade(investor_id)

    @login_required
    def delete(self, investor_id):
        FOFScaleAlteration.filter_by_query(investor_id=investor_id).delete()


class CustomerTradesSingle(ApiViewHandler):

    @login_required
    def put(self, trade_id):
        obj = FOFScaleAlteration.get_by_id(trade_id)
        update_trade(obj)

    @login_required
    def delete(self, trade_id):
        obj = FOFScaleAlteration.get_by_id(trade_id)
        obj.delete()


class CustomerFile(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def get(self):
        query = User.filter_by_query(role_id=StuffEnum.INVESTOR)
        df = pd.read_sql(query.statement, query.session.bind)

        out = io.BytesIO()
        writer = pd.ExcelWriter(out, engine='xlsxwriter')
        df.to_excel(excel_writer=writer, index=False, sheet_name='sheet0')
        writer.save()
        writer.close()
        file_name = datetime.datetime.now().strftime('%Y-%m-%d') + '.xlsx'
        response = make_response(out.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=%s" % file_name
        response.headers["Content-type"] = "application/x-xls"
        return response


class ResetStaffPassword(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def put(self, _id):
        password = request.json.get('password')
        password = password if password else '123456'
        user = User.filter_by_query(id=_id, role_id=StuffEnum.INVESTOR).first()
        if not user:
            raise VerifyError('不存在！')

        user_login = UserLogin.filter_by_query(user_id=user.id).one()
        user_login.password = password
        user_login.save()
        return 'success'


