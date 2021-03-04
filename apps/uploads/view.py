from flask import request, g
from utils.decorators import login_required
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError, LogicError
from extensions.s3.pdf_store import PdfStore


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


class ParsePDFAPI(ApiViewHandler):

    @login_required
    def post(self):
        """将私有文件路径转换为临时可访问路径"""

        file_key = request.json.get('file_key')
        if not file_key:
            raise VerifyError('No file_key')

        return PdfStore().create_pre_signed_url(object_name=file_key)
