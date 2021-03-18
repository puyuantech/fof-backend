
from bases.dbwrapper import db, BaseModel


class ContractTemplate(BaseModel):
    """合同模板"""
    __tablename__ = 'contract_template'

    template_id = db.Column(db.Integer, primary_key=True)
    fof_id = db.Column(db.String(16), index=True)
    manager_id = db.Column(db.String(32))
    template_type = db.Column(db.String(16))     # 模板类型: ContractTemplateType
    template_url_key = db.Column(db.String(128)) # 模板文件

    @classmethod
    def get_template_ids(cls, fof_id):
        templates = cls.filter_by_query(fof_id=fof_id).all()
        return {template.template_type: template.template_id for template in templates}

