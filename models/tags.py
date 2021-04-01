from bases.dbwrapper import db, BaseModel


class InvestorTag(BaseModel):
    """投资者标签标签"""
    __tablename__ = 'investor_tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    # 数据行编号
    tag_name = db.Column(db.String(16))                                 # 标签名称
    investor_id = db.Column(db.String(32))                              # 投资者ID
    manager_id = db.Column(db.String(32))                               # 管理端ID
    add_user_id = db.Column(db.Integer)                                 # 添加者ID
    del_user_id = db.Column(db.Integer)                                 # 删除者ID


class Tags(BaseModel):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 数据行编号
    tag_name = db.Column(db.String(16))  # 标签名称
    user_id = db.Column(db.Integer)  # 用户ID


class FOFLogos(BaseModel):
    """
    产品轮播图
    """
    __tablename__ = 'fof_logos'

    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.String(32))
    fof_id = db.Column(db.String(16))
    logo = db.Column(db.String(255))

