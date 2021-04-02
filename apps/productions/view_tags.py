
from flask import g
from bases.globals import db
from bases.exceptions import VerifyError
from bases.viewhandler import ApiViewHandler
from models import FOFTag
from utils.decorators import login_required, params_required
from sqlalchemy.sql import func


class ProTopTagsAPI(ApiViewHandler):

    @login_required
    def get(self):
        tag_names = db.session.query(
            FOFTag.tag_name
        ).filter_by(
            FOFTag.manager_id == g.token.manager_id,
            is_deleted=False
        ).group_by(
            FOFTag.tag_name
        ).order_by(
            func.count(FOFTag.id).desc()
        ).all()
        return [tag_name for tag_name, in tag_names]


class ProTagAPI(ApiViewHandler):

    @login_required
    @params_required(*['fof_id', 'tag_name'])
    def post(self):
        """添加标签"""
        if FOFTag.filter_by_query(
            tag_name=self.input.tag_name,
            fof_id=self.input.fof_id,
            manager_id=g.token.manager_id,
        ).one_or_none():
            raise VerifyError('标签已存在!')

        tag = FOFTag.create(
            tag_name=self.input.tag_name,
            fof_id=self.input.fof_id,
            manager_id=g.token.manager_id,
            add_user_id=g.user.id,
        )
        tag = FOFTag.get_by_id(tag.id)
        return tag.to_dict()

    @login_required
    @params_required(*['tag_id'])
    def delete(self):
        """删除标签"""
        tag = FOFTag.get_by_id(self.input.tag_id)
        tag.update(
            is_deleted=True,
            del_user_id=g.user.id,
        )
        return 'success'
