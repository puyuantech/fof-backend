import pandas as pd
import io
import datetime
import traceback
from flask import request, g, make_response
from sqlalchemy import distinct

from models import User, FOFInvestorPosition, FOFScaleAlteration, FOFInfo, UnitMap, \
    HedgeFundInvestorDivAndCarry, HedgeFundInvestorPurAndRedempSub, HedgeFundInvestorPurAndRedemp
from bases.globals import db
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from bases.constants import StuffEnum
from utils.helper import generate_sql_pagination, replace_nan
from utils.decorators import params_required, admin_login_required, login_required
from .libs import get_investor_info, register_investor_user, update_trade, parse_trade_file, \
    create_single_trade, parse_customer_file


class CusAPI(ApiViewHandler):

    @login_required
    def get(self):
        p = generate_sql_pagination()
        query = UnitMap.filter_by_query(
            manager_id=g.token.manager_id,
        )
        data = p.paginate(
            query,
            call_back=lambda x: [get_investor_info(i) for i in x],
            equal_filter=[UnitMap.cred, UnitMap.mobile, UnitMap.sponsor, UnitMap.status, UnitMap.salesman],
            range_filter=[UnitMap.sign_date],
            contains_filter=[UnitMap.name, UnitMap.mobile],
        )
        return data

    @login_required
    @params_required(*['mobile'])
    def post(self):
        if not self.is_valid_mobile(self.input.mobile):
            raise VerifyError('电话号码有误！')

        # 创建投资者
        unit_map = register_investor_user(
            self.input.mobile,
        )

        # 添加信息
        unit_map.update_columns(request)
        g.user_operation = '创建客户'
        g.user_operation_params = {
            'investor_id': unit_map.investor_id,
            'unit_map_id': unit_map.id,
        }
        return 'success'


class CusAdviserAPI(ApiViewHandler):

    @login_required
    def get(self):
        results = db.session.query(distinct(UnitMap.salesman)).all()
        data = [i[0] for i in results if i[0]]
        return data


class CusByFileAPI(ApiViewHandler):

    def get(self):
        df = pd.DataFrame(data=[], columns=['手机号码*', '姓名*', '证件类型*', '证件号码*', '通讯地址', '邮箱', '来源', '首次签约时间', '客户状态'])

        out = io.BytesIO()
        writer = pd.ExcelWriter(out, engine='xlsxwriter')
        df.to_excel(excel_writer=writer, index=False, sheet_name='sheet0')
        writer.save()
        file_name = 'investor_template.xlsx'
        response = make_response(out.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=%s" % file_name
        response.headers["Content-type"] = "application/x-xls"
        writer.close()
        return response

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def post(self):
        df = parse_customer_file()

        df['is_success'] = True
        df['failed_reason'] = ''

        for i in df.index:
            try:
                d = df.loc[i, :].to_dict()
                d = replace_nan(d)

                unit_map = register_investor_user(
                    d.get('mobile'),
                    get_map=True,
                )

                unit_map.name = d.get('name')
                unit_map.cred_type = d.get('cred_type')
                unit_map.cred = d.get('cred')
                unit_map.address = d.get('address')
                unit_map.email = d.get('email')
                unit_map.origin = d.get('origin')
                unit_map.sign_date = d.get('sign_date')
                unit_map.status = d.get('status')
                unit_map.save()

            except VerifyError as e:
                df['is_success'] = False
                df['failed_reason'] = e.msg
            except Exception as e:
                print(traceback.format_exc())
                df['is_success'] = False
                df['failed_reason'] = '创建错误'

        return replace_nan(df.to_dict(orient='records'))


class CustomerAPI(ApiViewHandler):

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def get(self, _id):
        instance = UnitMap.get_by_id(_id)
        if not instance:
            raise VerifyError('不存在！')
        return get_investor_info(instance)

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def put(self, _id):
        instance = UnitMap.get_by_id(_id)
        if not instance:
            raise VerifyError('不存在！')
        instance.update_columns(request)

        g.user_operation = '编辑客户'
        g.user_operation_params = {
            'investor_id': instance.investor_id,
            'unit_map_id': instance.id,
        }
        return get_investor_info(instance)

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def delete(self, _id):
        instance = UnitMap.get_by_id(_id)
        if not instance:
            raise VerifyError('不存在！')

        g.user_operation = '删除客户'
        g.user_operation_params = {
            'investor_id': instance.investor_id,
            'unit_map_id': instance.id,
        }
        instance.logic_delete()


class CustomerPositionSingle(ApiViewHandler):

    @login_required
    def get(self, investor_id):
        fof_id = request.args.get('fof_id')
        if not fof_id:
            raise VerifyError('No fof id')

        r = db.session.query(FOFInvestorPosition, FOFInfo).filter(
            FOFInvestorPosition.investor_id == investor_id,
            FOFInvestorPosition.manager_id == g.token.manager_id,
            FOFInfo.fof_id == FOFInvestorPosition.fof_id,
            FOFInvestorPosition.fof_id == fof_id,
        ).first()

        if not r:
            return {}

        d = r[0].to_dict()
        d['fof_name'] = r[1].fof_name
        d['net_asset_value'] = r[1].net_asset_value
        d['acc_unit_value'] = r[1].acc_unit_value
        d['ret_year_to_now'] = r[1].ret_year_to_now
        d['ret_total'] = r[1].ret_total

        return replace_nan(d)


class CustomerPosition(ApiViewHandler):

    @login_required
    def get(self, investor_id):

        results = db.session.query(FOFInvestorPosition, FOFInfo).filter(
            FOFInvestorPosition.investor_id == investor_id,
            FOFInvestorPosition.manager_id == g.token.manager_id,
            FOFInfo.fof_id == FOFInvestorPosition.fof_id,
            FOFInfo.is_deleted == False,
            FOFInfo.manager_id == g.token.manager_id,
        ).all()

        df_data = []
        for i in results:
            d = i[0].to_dict()
            d['fof_name'] = i[1].fof_name
            d['desc_name'] = i[1].desc_name
            d['net_asset_value'] = i[1].net_asset_value
            d['acc_unit_value'] = i[1].acc_unit_value
            d['ret_year_to_now'] = i[1].ret_year_to_now
            d['ret_total'] = i[1].ret_total
            df_data.append(d)

        df = pd.DataFrame(df_data)

        if len(df) < 1:
            return []

        df['sum_amount'] = df['amount'].sum()
        df['sum_total_ret'] = df['total_ret'].sum()
        df['sum_mv'] = df['mv'].sum()
        df['weight'] = df['mv'] / df['sum_mv']
        return replace_nan(df.to_dict(orient='records'))


class CustomerTrades(ApiViewHandler):

    @login_required
    def get(self, investor_id):
        event_type = request.args.get('event_type')
        if event_type:
            event_type = [int(i) for i in event_type.split(',')]
            results = db.session.query(FOFScaleAlteration, FOFInfo.fof_name, FOFInfo.desc_name).filter(
                FOFScaleAlteration.investor_id == investor_id,
                FOFScaleAlteration.manager_id == g.token.manager_id,
                FOFScaleAlteration.event_type.in_(event_type),
                FOFInfo.fof_id == FOFScaleAlteration.fof_id,
                FOFInfo.manager_id == g.token.manager_id,
            )
        else:
            results = db.session.query(FOFScaleAlteration, FOFInfo.fof_name, FOFInfo.desc_name).filter(
                FOFScaleAlteration.investor_id == investor_id,
                FOFScaleAlteration.manager_id == g.token.manager_id,
                FOFInfo.fof_id == FOFScaleAlteration.fof_id,
                FOFInfo.manager_id == g.token.manager_id,
            )
        df_list = []
        for i in results:
            d = i[0].to_dict()
            d['fof_name'] = i[1]
            d['desc_name'] = i[2]
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


class CustomerTradesPurRed(ApiViewHandler):

    def add_investor_info(self, data_dict: dict):
        fof_id = data_dict.get('fof_id')
        fof = FOFInfo.filter_by_query(
            fof_id=fof_id,
            manager_id=g.token.manager_id,
        ).first()
        if not fof:
            return None

        sub = HedgeFundInvestorPurAndRedempSub.filter_by_query(
            main_id=data_dict.get('id'),
        ).first()
        if sub:
            data_dict['trade_confirm_url'] = sub.trade_confirm_url
            data_dict['trade_apply_url'] = sub.trade_apply_url
            data_dict['remark'] = sub.remark

        data_dict['fof_name'] = fof.fof_name
        data_dict['desc_name'] = fof.desc_name
        return data_dict

    @login_required
    def get(self, investor_id):
        p = generate_sql_pagination()
        query = HedgeFundInvestorPurAndRedemp.filter_by_query(
            investor_id=investor_id,
            manager_id=g.token.manager_id,
        )
        data = p.paginate(
            query,
            call_back=lambda x: [self.add_investor_info(i.to_dict()) for i in x if self.add_investor_info(i.to_dict())],
            equal_filter=[
                HedgeFundInvestorPurAndRedemp.event_type,
                HedgeFundInvestorPurAndRedemp.fof_id,
            ],
        )
        return data


class CustomerTradesDivCar(ApiViewHandler):

    def add_investor_info(self, data_dict: dict):
        fof_id = data_dict.get('fof_id')
        fof = FOFInfo.filter_by_query(
            fof_id=fof_id,
            manager_id=g.token.manager_id,
        ).first()
        if not fof:
            return None

        data_dict['fof_name'] = fof.fof_name
        data_dict['desc_name'] = fof.desc_name
        return data_dict

    @login_required
    def get(self, investor_id):
        p = generate_sql_pagination()
        query = HedgeFundInvestorDivAndCarry.filter_by_query(
            investor_id=investor_id,
            manager_id=g.token.manager_id,
        )
        data = p.paginate(
            query,
            call_back=lambda x: [self.add_investor_info(i.to_dict()) for i in x if self.add_investor_info(i.to_dict())],
            equal_filter=[HedgeFundInvestorDivAndCarry.event_type],
        )
        return data


class CustomerTradesSingle(ApiViewHandler):

    @login_required
    def get(self, trade_id):
        obj = HedgeFundInvestorPurAndRedemp.get_by_id(trade_id)
        return obj.to_dict()

    @login_required
    def put(self, trade_id):
        obj = HedgeFundInvestorPurAndRedemp.get_by_id(trade_id)
        update_trade(obj)

    @login_required
    def delete(self, trade_id):
        obj = HedgeFundInvestorPurAndRedemp.get_by_id(trade_id)
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

        user.password = password
        user.save()
        return 'success'

