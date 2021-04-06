
import datetime
from flask import request, g
from bases.view_mixin import *
from bases.viewhandler import ApiViewHandler
from models import InfoDetail, InfoTemplate
from utils.decorators import params_required
from .libs import get_info_production, update_info_production


class InformationAPI(ApiViewHandler, ViewList):
    model = InfoDetail

    @login_required
    def get(self):
        p = generate_sql_pagination()

        query = InfoDetail.filter_by_query(manager_id=g.token.manager_id)
        data = p.paginate(
            query,
            call_back=lambda x: [get_info_production(i) for i in x],
            equal_filter=[InfoDetail.title, InfoDetail.info_type, InfoDetail.is_effected],
            range_filter=[InfoDetail.create_time],
        )
        return data

    @params_required(*['title', 'info_type'])
    @login_required
    def post(self):
        obj = InfoDetail.create(
            title=self.input.title,
            author=request.json.get('author'),
            thumbnail=request.json.get('thumbnail'),
            summary=request.json.get('summary'),
            sub_file=request.json.get('sub_file'),
            info_type=self.input.info_type,
            content_type=request.json.get('content_type'),
            is_effected=request.json.get('is_effected'),
            content=request.json.get('content'),
            effect_user_name=request.json.get('effect_user_name'),
            effect_time=request.json.get('effect_time'),
            create_user_id=g.user.id,
            manager_id=g.token.manager_id,
        )
        update_info_production(obj)

        g.user_operation = '删除咨询'
        g.user_operation_params = {
            'id': obj.id,
        }


class InformationDetailAPI(ApiViewHandler, ViewDetailGet, ViewDetailUpdate, ViewDetailDelete):
    model = InfoDetail
    update_columns = [
        'title',
        'author',
        'thumbnail',
        'summary',
        'sub_file',
        'info_type',
        'content_type',
        'content',
        'is_effected',
        'effect_user_name',
        'effect_time',
    ]

    @login_required
    def get(self, _id):
        obj = self.model.get_by_id(_id)
        data = get_info_production(obj)
        return data

    @login_required
    def put(self, _id):
        obj = self.model.get_by_id(_id)

        for i in self.update_columns:
            if request.json.get(i) is not None:
                obj.update(commit=False, **{i: request.json.get(i)})
        obj.save()
        update_info_production(obj)
        return

    @login_required
    def delete(self, _id):
        obj = self.model.get_by_id(_id)
        obj.logic_delete()
        g.user_operation = '删除咨询'
        g.user_operation_params = {
            'id': _id,
        }
        return


class TemplateAPI(ApiViewHandler, ViewList):
    model = InfoTemplate

    def get_objects(self):
        return self.model.filter_by_query(manager_id=g.token.manager_id)

    @params_required(*['template_name'])
    @login_required
    def post(self):
        InfoTemplate.create(
            manager_id=g.token.manager_id,
            template_name=self.input.template_name,
            content=request.json.get('content'),
        )


class TemplateDetailAPI(ApiViewHandler, ViewDetailGet, ViewDetailUpdate, ViewDetailDelete):
    model = InfoTemplate
    update_columns = [
        'template_name',
        'content',
    ]
