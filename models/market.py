from bases.dbwrapper import db, BaseModel
from sqlalchemy.dialects.mysql import DOUBLE


class CustomIndex(BaseModel):
    """
    自定义指数
    """
    __tablename__ = 'custom_index'

    id = db.Column(db.Integer, primary_key=True)                                # 编号
    name = db.Column(db.String(31))                                             # 名称
    nav = db.Column(db.CHAR(64), default='')                                    # 净值

