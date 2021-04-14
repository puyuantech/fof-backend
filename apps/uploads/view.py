import re

from flask import request, g

from bases.exceptions import LogicError, VerifyError
from bases.viewhandler import ApiViewHandler
from extensions.s3.image_store import ImageStore
from extensions.s3.pdf_store import PdfStore
from extensions.s3.public_file_store import FileStore
from extensions.s3.private_file_store import FileStore as PriFileStore
from utils.decorators import login_required, params_required


class UploadPublicFileAPI(ApiViewHandler):

    @login_required
    def post(self):
        """上传公共文件"""
        file_obj = request.files.get('file')
        content_type = request.args.get('content_type')
        if not file_obj:
            raise VerifyError('没有文件！')
        if not content_type:
            raise VerifyError('未指定文件类型！')

        file_suffix = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', file_obj.filename)[0]
        file_key, url = FileStore().store_file_from_user(g.user.id, file_obj, content_type, file_suffix)
        if not file_key:
            raise LogicError('store file failed! (err_msg){}'.format(url))
        return {
            'url': url
        }


class UploadPrivateFileAPI(ApiViewHandler):

    @login_required
    def post(self):
        """上传私有文件"""
        file_obj = request.files.get('file')

        content_type = request.args.get('content_type')
        if not file_obj:
            raise VerifyError('没有文件！')
        if not content_type:
            raise VerifyError('未指定文件类型！')

        file_suffix = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', file_obj.filename)[0]
        file_key, url = PriFileStore().store_file_from_user(g.user.id, file_obj, content_type, file_suffix)
        if not file_key:
            raise LogicError('store file failed! (err_msg){}'.format(url))
        return {
            'file_key': file_key
        }


class UploadPDFAPI(ApiViewHandler):

    @login_required
    def post(self):
        """上传PDF文件"""
        file_obj = request.files.get('file')
        if not file_obj:
            raise VerifyError('没有文件！')
        file_key, img = PdfStore().store_pdf_from_user(g.user.id, file_obj)
        if not file_key:
            raise LogicError('store head img failed! (err_msg){}'.format(img))
        return {
            'file_key': file_key
        }


class UploadImageAPI(ApiViewHandler):

    @login_required
    def post(self):
        """上传图片"""
        file_obj = request.files.get('file')
        file_key = ImageStore.store_image_from_user(g.user.id, file_obj)
        return {'file_key': file_key}


class ParsePDFAPI(ApiViewHandler):

    @login_required
    def post(self):
        """将私有文件路径转换为临时可访问路径"""

        file_key = request.json.get('file_key')
        if not file_key:
            raise VerifyError('No file_key')

        return PdfStore().create_pre_signed_url(object_name=file_key)
