from bases.dbwrapper import db, BaseModel


class UserTag(BaseModel):
    """用户标签"""
    __tablename__ = 'user_tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    # 数据行编号
    tag_name = db.Column(db.String(16))                                 # 标签名称
    user_id = db.Column(db.Integer)                                     # 用户ID
    add_user_id = db.Column(db.Integer)                                 # 添加者ID
    del_user_id = db.Column(db.Integer)                                 # 删除者ID


class Tags(BaseModel):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 数据行编号
    tag_name = db.Column(db.String(16))  # 标签名称
    user_id = db.Column(db.Integer)  # 用户ID

