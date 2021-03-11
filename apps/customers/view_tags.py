
from flask import g, request

from flask import g
from bases.globals import db
from bases.exceptions import VerifyError
from bases.viewhandler import ApiViewHandler
from models import InvestorTag, InvestorInfo
from utils.decorators import login_required, params_required
from sqlalchemy.sql import func


class TagsAPI(ApiViewHandler):

    @login_required
    def get(self):
        tag_names = request.args.get('tag_names', '').split(',')
        if not tag_names:
            return []

        investors = db.session.query(
            InvestorTag,
        ).filter(
            InvestorTag.tag_name.in_(tag_names),
            InvestorInfo.investor_id == InvestorTag.investor_id,
            InvestorTag.manager_id == g.token.manager_id,
        ).group_by(
            InvestorTag.investor_id
        ).all()

        return [i.to_dict() for i in investors]


class TopTagsAPI(ApiViewHandler):

    @login_required
    def get(self):
        tag_names = db.session.query(
            InvestorTag.tag_name
        ).filter_by(
            InvestorTag.manager_id == g.token.manager_id,
            is_deleted=False
        ).group_by(
            InvestorTag.tag_name
        ).order_by(
            func.count(InvestorTag.id).desc()
        ).all()
        return [tag_name for tag_name, in tag_names]


class TagAPI(ApiViewHandler):

    @login_required
    @params_required(*['investor_id', 'tag_name'])
    def post(self):
        """添加标签"""
        if InvestorTag.filter_by_query(
            tag_name=self.input.tag_name,
            investor_id=self.input.investor_id,
            manager_id=g.token.manager_id,
        ).one_or_none():
            raise VerifyError('标签已存在!')

        tag = InvestorTag.create(
            tag_name=self.input.tag_name,
            invinvestor_id=self.input.investor_id,
            manager_id=g.token.manager_id,
            add_user_id=g.user.id,
        )
        tag = InvestorTag.get_by_id(tag.id)
        return tag.to_dict()

    @login_required
    @params_required(*['tag_id'])
    def delete(self):
        """删除标签"""
        tag = InvestorTag.get_by_id(self.input.tag_id)
        tag.update(
            is_deleted=True,
            del_user_id=g.user.id,
        )
        return 'success'
