
from flask import g, request

from bases.globals import db
from bases.exceptions import VerifyError
from bases.viewhandler import ApiViewHandler
from models import UserTag, User
from utils.decorators import login_required, params_required
from sqlalchemy.sql import func


class TagsAPI(ApiViewHandler):

    @login_required
    def get(self):
        tag_names = request.args.get('tag_names', '').split(',')
        if not tag_names:
            return []

        users = db.session.query(
            User,
        ).filter(
            UserTag.tag_name.in_(tag_names),
            User.id == UserTag.user_id,
        ).group_by(
            UserTag.user_id
        ).all()

        return [i.to_cus_dict() for i in users]


class TopTagsAPI(ApiViewHandler):

    @login_required
    def get(self):
        tag_names = db.session.query(
            UserTag.tag_name
        ).filter_by(is_deleted=False).group_by(
            UserTag.tag_name
        ).order_by(
            func.count(UserTag.id).desc()
        ).all()
        return [tag_name for tag_name, in tag_names]


class TagAPI(ApiViewHandler):

    @login_required
    @params_required(*['user_id', 'tag_name'])
    def post(self):
        """添加标签"""
        if UserTag.filter_by_query(
            tag_name=self.input.tag_name,
            user_id=self.input.user_id,
        ).one_or_none():
            raise VerifyError('标签已存在!')

        user_tag = UserTag.create(
            tag_name=self.input.tag_name,
            user_id=self.input.user_id,
            add_user_id=g.user.id,
        )
        user_tag = UserTag.get_by_id(user_tag.id)
        return user_tag.to_dict()

    @login_required
    @params_required(*['tag_id'])
    def delete(self):
        """删除标签"""
        user_tag = UserTag.get_by_id(self.input.tag_id)
        user_tag.update(
            is_deleted=True,
            del_user_id=g.user.id,
        )
        return 'success'

