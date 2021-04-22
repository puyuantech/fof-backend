import traceback
from flask import g, request, current_app
from bases.viewhandler import ApiViewHandler
from bases.globals import db
from bases.exceptions import VerifyError
from bases.constants import StuffEnum
from models import ManagerInfo, User, ManagerUserMap, ApplyFile, ApplyStatus
from apps.admin_super.decorators import admin_super_login_required
from utils.decorators import params_required
from utils.helper import generate_sql_pagination


class ManagersAPI(ApiViewHandler):

    @admin_super_login_required
    def get(self):
        p = generate_sql_pagination()
        query = ManagerInfo.filter_by_query()
        data = p.paginate(query)
        return data

    @admin_super_login_required
    @params_required(*['manager_id', 'name', 'admin_username', 'admin_password'])
    def post(self):
        if ManagerInfo.filter_by_query(
            manager_id=self.input.manager_id,
            show_deleted=True,
        ).first():
            raise VerifyError('组织机构代码已存在')

        if User.filter_by_query(
            username=self.input.admin_username,
        ).first():
            raise VerifyError('用户名已存在')

        u = User.create(
            username=self.input.admin_username,
            password=self.input.admin_password,
            role_id=StuffEnum.ADMIN,
            is_staff=True,
        )
        try:
            m = ManagerInfo(
                manager_id=self.input.manager_id,
                name=self.input.name,
                id_type=request.json.get('id_type'),
                id_number=request.json.get('id_number'),
                address=request.json.get('address'),
                legal_person=request.json.get('legal_person'),
            )
            m_map = ManagerUserMap(
                user_id=u.id,
                manager_id=self.input.manager_id,
            )
            db.session.add(m)
            db.session.add(m_map)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            u.delete()
            current_app.logger.error(traceback.format_exc())
        return


class ManagerAPI(ApiViewHandler):
    model = ManagerInfo
    update_columns = [
        'name',
        'id_type',
        'id_number',
        'address',
        'legal_person',
    ]

    def get_object(self, _id):
        return self.model.get_by_query(manager_id=_id)

    @admin_super_login_required
    def get(self, _id):
        obj = self.get_object(_id)
        return obj.to_dict()

    @admin_super_login_required
    def delete(self, _id):
        obj = self.get_object(_id)
        obj.delete()

    @admin_super_login_required
    def put(self, _id):
        obj = self.get_object(_id)
        for i in self.update_columns:
            if request.json.get(i) is not None:
                obj.update(commit=False, **{i: request.json.get(i)})
        obj.save()
        return


class SignAppliesAPI(ApiViewHandler):

    @admin_super_login_required
    def get(self):
        p = generate_sql_pagination()
        query = ApplyFile.filter_by_query(
            sign_stage=2,
        )
        data = p.paginate(
            query,
            equal_filter=[ApplyFile.sign_status]
        )
        return data


class SignStatusAPI(ApiViewHandler):

    @admin_super_login_required
    def get(self, _id):
        obj = ApplyStatus.get_by_id(_id)
        return obj.to_dict()

    @admin_super_login_required
    def put(self, _id):
        obj = ApplyStatus.get_by_id(_id)

        update_columns = [
            'manager_cred',
            'lp_cred',
            'admin_cred',
            'service_cred',
            'hf_success',
        ]
        for i in update_columns:
            if i in request.json:
                ApplyStatus.update(
                    commit=False,
                    **{
                        i: request.json.get(i)
                    },
                )
        obj.save()
        return 'success'


class SignApplyAPI(ApiViewHandler):

    @params_required(*['sign_status'])
    @admin_super_login_required
    def put(self, _id):
        obj = ApplyStatus.get_by_id(_id)
        if not all([obj.manager_cred, obj.lp_cred, obj.admin_cred, obj.service_cred, obj.hf_success]):
            raise VerifyError('认证流程未完成')

        if self.input.sign_status == ApplyFile.SignEnum.SUCCESS:
            obj.sign_status = ApplyFile.SignEnum.SUCCESS
            obj.save()
            return

        if self.input.sign_status == ApplyFile.SignEnum.FAILED:
            failed_reason = request.json.get('failed_reason')
            if not failed_reason:
                VerifyError('请填写失败原因！')
            obj.sign_status = ApplyFile.SignEnum.FAILED
            obj.failed_reason = failed_reason
            return
