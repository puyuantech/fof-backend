import pandas as pd
import traceback
import datetime
from flask import request, current_app

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from models import CustomIndex, CustomIndexNav
from utils.decorators import params_required
from utils.helper import generate_sql_pagination, replace_nan
from .libs import update_custom_index_info, update_custom_index_ratios

from surfing.util.calculator import Calculator as SurfingCalculator


class IndexListAPI(ApiViewHandler):

    def get(self):
        p = generate_sql_pagination()
        query = CustomIndex.filter_by_query()
        data = p.paginate(query)
        return data

    @params_required(*['name', 'desc'])
    def post(self):
        CustomIndex.create(
            name=self.input.name,
            desc=self.input.desc,
        )
        return 'success'


class IndexAPI(ApiViewHandler):
    def get(self, _id):
        obj = CustomIndex.get_by_query(id=_id)
        return obj.to_dict()

    def put(self, _id):
        obj = CustomIndex.get_by_query(id=_id)
        update_custom_index_info(obj)
        return

    def delete(self, _id):
        obj = CustomIndex.get_by_query(id=_id)
        obj.logic_delete()

    @params_required(*['method'])
    def post(self, _id):
        obj = CustomIndex.get_by_query(id=_id)

        req_file = request.files.get('file')
        if not req_file:
            raise VerifyError('Couldn\'t find any uploaded file')

        # 解析文件
        try:
            df = pd.read_csv(
                req_file,
                index_col=None,
                dtype={'日期': str, '点数': float},
            )
            df = df[['日期', '点数']]
            df['日期'] = df['日期'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())
            df = df.rename(columns={
                '日期': 'datetime',
                '点数': 'nav',
            })
            df['index_id'] = _id
        except:
            current_app.logger.error(traceback.format_exc())
            raise VerifyError('解析失败')

        # 完全覆盖
        if self.input.method == 'all':
            ratios = SurfingCalculator.get_stat_result_from_df(df, 'datetime', 'nav')
            update_custom_index_ratios(obj, ratios)

            CustomIndexNav.filter_by_query(index_id=obj.id).delete()
            db.session.execute(
                CustomIndexNav.__table__.insert(),
                df.to_dict(orient='r'),
            )
            db.session.commit()
            return 'success'

        # 部分覆盖
        if self.input.method == 'part':
            db.session.query(CustomIndexNav).filter(
                CustomIndexNav.index_id == obj.id,
                CustomIndexNav.datetime.in_(df['datetime'].to_list())
            ).delete(synchronize_session=False)
            db.session.execute(
                CustomIndexNav.__table__.insert(),
                df.to_dict(orient='records'),
            )
            db.session.commit()

            # 跟新指标
            query = db.session.query(CustomIndexNav).filter(
                CustomIndexNav.index_id == obj.id,
            )
            df = pd.read_sql(query.statement, query.session.bind)
            ratios = SurfingCalculator.get_stat_result_from_df(df, 'datetime', 'nav')
            update_custom_index_ratios(obj, ratios)
            db.session.commit()

            return 'success'
        raise VerifyError('参数错误')


class IndexDetailAPI(ApiViewHandler):
    def get(self, _id):
        query = db.session.query(CustomIndexNav).filter(
            CustomIndexNav.index_id == _id,
        )
        df = pd.read_sql(query.statement, query.session.bind)
        df = df.reset_index()
        if len(df) < 1:
            return {}

        data = {
            'dates': df['datetime'].to_list(),
            'values': df['nav'].to_list(),
            'ratios': SurfingCalculator.get_stat_result_from_df(df, 'datetime', 'nav').__dict__,
        }
        return replace_nan(data)


class IndexSingleChangeAPI(ApiViewHandler):

    @params_required(*['index_id', 'datetime', 'new_data'])
    def post(self):
        date = datetime.datetime.strptime(
            self.input.datetime,
            '%Y-%m-%d'
        )
        obj = CustomIndexNav.filter_by_query(
            index_id=self.input.index_id,
            datetime=date,
        ).one_or_none()
        if not obj:
            raise VerifyError('修改目标不存在！')
        obj.nav = self.input.new_data
        obj.save()

        # 跟新指标
        query = db.session.query(CustomIndexNav).filter(
            CustomIndexNav.index_id == self.input.index_id,
        )
        df = pd.read_sql(query.statement, query.session.bind)
        print(df)
        ratios = SurfingCalculator.get_stat_result_from_df(df, 'datetime', 'nav')
        update_custom_index_ratios(obj, ratios)
        db.session.commit()
        return

