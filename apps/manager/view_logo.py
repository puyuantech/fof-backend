
from flask import g
from bases.viewhandler import ApiViewHandler
from models import FOFInfo, FOFLogos, ManagerInfo
from utils.decorators import login_required, params_required


class LogoAPI(ApiViewHandler):

    @params_required(*['manager_id'])
    @login_required
    def get(self):
        manager_info = ManagerInfo.get_by_query(manager_id=self.input.manager_id)
        return manager_info.logo

    @params_required(*['manager_id', 'logo'])
    @login_required
    def put(self):
        manager_info = ManagerInfo.get_by_query(manager_id=self.input.manager_id)
        manager_info.update(logo=self.input.logo)
        g.user_operation = '修改logo'
        return 'success'


class FOFLogoAPI(ApiViewHandler):

    @params_required(*['manager_id', 'fof_id', 'logo'])
    @login_required
    def post(self):
        FOFLogos.create(
            manager_id=self.input.manager_id,
            fof_id=self.input.fof_id,
            logo=self.input.logo,
        )
        g.user_operation = '创建轮播图'
        return 'success'

    @params_required(*['logo_id', 'fof_id', 'logo'])
    @login_required
    def put(self):
        fof_logo = FOFLogos.get_by_id(self.input.logo_id)
        fof_logo.update(fof_id=self.input.fof_id, logo=self.input.logo)
        g.user_operation = '修改轮播图'
        return 'success'

    @params_required(*['logo_id'])
    @login_required
    def delete(self):
        fof_logo = FOFLogos.get_by_id(self.input.logo_id)
        fof_logo.logic_delete()
        g.user_operation = '删除轮播图'
        return 'success'


class FOFLogoListAPI(ApiViewHandler):

    @params_required(*['manager_id'])
    @login_required
    def get(self):
        fof_logos = FOFLogos.filter_by_query(manager_id=self.input.manager_id).all()
        fofs = FOFInfo.filter_by_query(manager_id=self.input.manager_id).all()
        fofs = {fof.fof_id: fof.fof_name for fof in fofs}

        data = []
        for fof_logo in fof_logos:
            data.append({
                'fof_name': fofs.get(fof_logo.fof_id),
                **fof_logo.to_dict()
            })
        return data

