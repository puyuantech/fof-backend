from bases.dbwrapper import db, BaseModel


class InfoDetail(BaseModel):
    __tablename__ = 'info_detail'

    type_choices = [
        (1, '路演'),
        (2, '观点'),
        (3, '问答'),
        (4, '公告'),
        (5, '报告'),
    ]

    content_type_choices = [
        (1, 'template'),
        (2, 'rick_text'),
        (3, 'file_key'),
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)            # 编号
    title = db.Column(db.String(63))                                            # 标题
    info_type = db.Column(db.Integer)                                           # 类型
    content_type = db.Column(db.Integer)                                        # 内容类型
    content = db.Column(db.TEXT)                                                # 内容
    is_effected = db.Column(db.BOOLEAN, default=False)                          # 是否上架
    effect_time = db.Column(db.DATETIME)                                        # 上架时间
    effect_user_name = db.Column(db.String(63))                                   # 上架人姓名
    create_user_id = db.Column(db.Integer)                                      # 创建人ID
    manager_id = db.Column(db.String(32))                                       # 管理者ID


class InfoToProduction(BaseModel):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)            # 编号
    info_id = db.Column(db.Integer)                                             # 资讯ID
    fof_id = db.Column(db.CHAR(16))                                             # 产品ID


class InfoTemplate(BaseModel):
    __tablename__ = 'info_templates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)            # 编号
    content = db.Column(db.TEXT)                                                # 配置
