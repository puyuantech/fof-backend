
from bases.constants import TemplateStatus
from bases.dbwrapper import db, BaseModel


class ProductionTemplate(BaseModel):
    """产品合同模板状态"""
    __tablename__ = 'production_template'

    id = db.Column(db.Integer, primary_key=True)
    fof_id = db.Column(db.String(16))
    manager_id = db.Column(db.String(32))
    template_status = db.Column(db.String(16))

    def get_detail(self):
        templates = []
        if self.template_status in (TemplateStatus.SIGNING, TemplateStatus.COMPLETED):
            templates = ContractTemplate.get_templates(self.fof_id, self.manager_id)
            if self.template_status == TemplateStatus.SIGNING and all(template['signed'] for template in templates):
                self.update(template_status=TemplateStatus.COMPLETED)

        db.session.refresh(self)
        data = self.to_dict()
        data['templates'] = templates
        return data

    @classmethod
    def fill_template_status(cls, manager_id, fof_infos):
        fof_ids = cls.filter_by_query(manager_id=manager_id).all()
        fof_ids = {fof_id.fof_id: fof_id.template_status for fof_id in fof_ids}

        for fof_info in fof_infos:
            fof_info['template_status'] = fof_ids.get(fof_info['fof_id'], TemplateStatus.NOSTART)
        return fof_infos


class ContractTemplate(BaseModel):
    """合同模板"""
    __tablename__ = 'contract_template'

    template_id = db.Column(db.Integer, primary_key=True)
    fof_id = db.Column(db.String(16), index=True)
    manager_id = db.Column(db.String(32))
    template_type = db.Column(db.String(16))     # 模板类型: ContractTemplateType
    template_url_key = db.Column(db.String(128)) # 模板文件
    signed = db.Column(db.Boolean)               # 是否签署

    @classmethod
    def get_template_ids(cls, fof_id):
        templates = cls.filter_by_query(fof_id=fof_id).all()
        return {template.template_type: template.template_id for template in templates}

    @classmethod
    def get_templates(cls, fof_id, manager_id):
        templates = cls.filter_by_query(fof_id=fof_id, manager_id=manager_id).all()
        return [template.to_dict() for template in templates]

