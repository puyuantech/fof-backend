from bases.dbwrapper import db, BaseModel
from sqlalchemy_utils import ChoiceType


class InfoDetail(BaseModel):
    __tablename__ = 'info_detail'

    types_choices = [
        (1, 'template'),
        (2, 'rick_text'),
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)            # 编号
    content = db.Column(db.TEXT)                                                # 内容
    type = db.Column(ChoiceType(types_choices))                                 # 类型


class InfoTemplate(BaseModel):
    __tablename__ = 'info_templates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)            # 编号
    content = db.Column(db.TEXT)                                                # 配置
