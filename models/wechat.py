from bases.dbwrapper import db, BaseModel


class WeChatUnionID(BaseModel):
    """用户微信绑定"""
    __tablename__ = "user_we_chat"

    id = db.Column(db.Integer, primary_key=True)                        # 编号
    union_id = db.Column(db.CHAR(128))                                  # 微信开放平台
    open_id = db.Column(db.CHAR(128), default='')                       # 公众号(服务号)
    manager_id = db.Column(db.String(32))                               # 管理ID
    nick_name = db.Column(db.String(127))
    avatar_url = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='we_chat')

    def to_doc_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nick_name': self.nick_name,
            'avatar_url': self.avatar_url,
        }


class WeChatToken(BaseModel):
    """微信 access token 和 jsapi_ticket"""
    __tablename__ = "wechat_token"

    id = db.Column(db.Integer, primary_key=True)                                # 编号
    key = db.Column(db.CHAR(255))                                               # token 值
    expires_at = db.Column(db.DATETIME, nullable=False)                         # 过期时间
    token_type = db.Column(db.CHAR(32))                                         # access_token | jsapi_ticket
    manager_id = db.Column(db.String(32), unique=True)

