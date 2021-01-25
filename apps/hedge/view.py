import pandas as pd
import traceback
import datetime
from flask import request, current_app

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from bases.constants import StuffEnum
from models import HedgeFundInfo, HedgeFundNAV, HedgeComment
from utils.decorators import params_required, login_required, admin_login_required
from utils.helper import generate_sql_pagination, replace_nan

from surfing.util.calculator import Calculator as SurfingCalculator
from surfing.data.manager.manager_fof import FOFDataManager

from .libs import update_hedge_fund_info, make_hedge_fund_info, update_hedge_value


class HedgesAPI(ApiViewHandler):

    @login_required
    def get(self):
        p = generate_sql_pagination()
        query = HedgeFundInfo.filter_by_query()
        data = p.paginate(query, call_back=lambda x: [make_hedge_fund_info(i) for i in x])

        return data

    @login_required
    @params_required(*['fund_id'])
    def post(self):
        data = {
            'fund_id': request.json.get('fund_id'),
            'fund_name': request.json.get('fund_name'),
            'manager_id': request.json.get('manager_id'),
            'water_line': request.json.get('water_line'),
            'brief_name': request.json.get('brief_name'),
            'incentive_fee_mode': request.json.get('incentive_fee_mode'),
            'incentive_fee_ratio': request.json.get('incentive_fee_ratio'),
            'v_nav_decimals': request.json.get('v_nav_decimals'),
        }
        if HedgeFundInfo.filter_by_query(fund_id=self.input.fund_id).one_or_none():
            raise VerifyError('ID 重复')
        obj = HedgeFundInfo.create(**data)
        update_hedge_fund_info(obj)
        return


class HedgeCommentAPI(ApiViewHandler):
    @login_required
    @params_required(*['comment'])
    def post(self, _id):
        HedgeComment.create(
         fund_id=_id,
         comment=self.input.comment,
        )
        return


class HedgeDetail(ApiViewHandler):
    @login_required
    def get(self, _id):
        results = db.session.query(HedgeFundNAV).filter(
            HedgeFundNAV.fund_id == _id,
        ).all()
        # results = HedgeFundNAV.filter_by_query(
        #     fund_id=_id,
        # ).all()
        df = pd.DataFrame([i.to_dict() for i in results])
        df = df.reset_index()

        if len(df) < 1:
            return {}

        data = {
            'dates': df['datetime'].to_list(),
            'v_net_value': df['v_net_value'].to_list(),
            'net_asset_value': df['net_asset_value'].to_list(),
            'acc_unit_value': df['acc_unit_value'].to_list(),
            'ratios': {},
        }

        df = df.dropna(subset=['v_net_value'])
        if len(df) < 1:
            return data

        data['ratios'] = SurfingCalculator.get_stat_result_from_df(df, 'datetime', 'v_net_value').__dict__
        return replace_nan(data)

    @login_required
    def post(self, _id):
        obj = HedgeFundInfo.get_by_query(fund_id=_id)

        req_file = request.files.get('file')
        if not req_file:
            raise VerifyError('Couldn\'t find any uploaded file')

        status = FOFDataManager.upload_hedge_nav_data(
            req_file.read(),
            req_file.name,
            _id,
        )
        if not status:
            raise VerifyError('上传失败！')

    @admin_login_required([StuffEnum.ADMIN, StuffEnum.FUND_MANAGER, StuffEnum.OPE_MANAGER])
    def delete(self, _id):
        HedgeFundInfo.get_by_query(fund_id=_id)
        HedgeFundNAV.filter_by_query(fund_id=_id).delete()


class HedgeAPI(ApiViewHandler):
    @login_required
    def get(self, _id):
        obj = HedgeFundInfo.get_by_query(fund_id=_id)
        data = make_hedge_fund_info(obj)
        return data

    @login_required
    def put(self, _id):
        obj = HedgeFundInfo.get_by_query(fund_id=_id)
        update_hedge_fund_info(obj)
        return

    @login_required
    def delete(self, _id):
        obj = HedgeFundInfo.get_by_query(fund_id=_id)
        obj.logic_delete()

    # @login_required
    # @params_required(*['method'])
    # def post(self, _id):
    #     obj = HedgeFundInfo.get_by_query(fund_id=_id)
    #
    #     req_file = request.files.get('file')
    #     if not req_file:
    #         raise VerifyError('Couldn\'t find any uploaded file')
    #
    #     # 解析文件
    #     try:
    #         df = pd.read_csv(
    #             req_file,
    #             index_col=None,
    #             dtype={'日期': str, '累计净值': float, '单位净值': float, '虚拟净值': float},
    #         )
    #         df = df[['日期', '累计净值', '单位净值', '虚拟净值']]
    #         df['日期'] = df['日期'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())
    #         df = df.rename(columns={
    #             '日期': 'datetime',
    #             '累计净值': 'acc_unit_value',
    #             '单位净值': 'net_asset_value',
    #             '虚拟净值': 'v_net_value',
    #         })
    #         df['fund_id'] = _id
    #         df['insert_time'] = datetime.datetime.now().date()
    #     except:
    #         current_app.logger.error(traceback.format_exc())
    #         raise VerifyError('解析失败')
    #
    #     # 完全覆盖
    #     if self.input.method == 'all':
    #         HedgeFundNAV.filter_by_query(fund_id=_id).delete()
    #         db.session.execute(
    #             HedgeFundNAV.__table__.insert(),
    #             df.to_dict(orient='r'),
    #         )
    #         db.session.commit()
    #         update_hedge_value(_id)
    #         return 'success'
    #
    #     # 部分覆盖
    #     if self.input.method == 'part':
    #         db.session.query(HedgeFundNAV).filter(
    #             HedgeFundNAV.fund_id == _id,
    #             HedgeFundNAV.datetime.in_(df['datetime'].to_list())
    #         ).delete(synchronize_session=False)
    #         db.session.execute(
    #             HedgeFundNAV.__table__.insert(),
    #             df.to_dict(orient='records'),
    #         )
    #         db.session.commit()
    #         update_hedge_value(_id)
    #         return 'success'
    #     raise VerifyError('参数错误')


class HedgeSingleChangeAPI(ApiViewHandler):
    @login_required
    @params_required(*['fund_id', 'datetime', 'net_asset_value', 'acc_unit_value', 'v_net_value'])
    def post(self):
        date = datetime.datetime.strptime(
            self.input.datetime,
            '%Y-%m-%d'
        )
        obj = HedgeFundNAV.filter_by_query(
            fund_id=self.input.fund_id,
            datetime=date,
        ).one_or_none()
        if not obj:
            raise VerifyError('修改目标不存在！')

        obj.net_asset_value = self.input.net_asset_value
        obj.acc_unit_value = self.input.acc_unit_value
        obj.v_net_value = self.input.v_net_value
        obj.save()
        update_hedge_value(self.input.fund_id)
        return

    @login_required
    @params_required(*['fund_id', 'datetime'])
    def delete(self):
        date = datetime.datetime.strptime(
            self.input.datetime,
            '%Y-%m-%d'
        )
        obj = HedgeFundNAV.filter_by_query(
            fund_id=self.input.fund_id,
            datetime=date,
        ).one_or_none()
        if not obj:
            raise VerifyError('修改目标不存在！')

        obj.net_asset_value = self.input.net_asset_value
        obj.acc_unit_value = self.input.acc_unit_value
        obj.v_net_value = self.input.v_net_value
        obj.save()
        update_hedge_value(self.input.fund_id)
        return

