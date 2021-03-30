
import datetime
import os
import traceback
import uuid

from bases.exceptions import LogicError
from bases.globals import settings
from extensions.s3.s3_client import S3Connector


class LogStore:

    store_path = settings['TEMP_PATH']
    public_bucket_name = settings['AWS_PUBLIC_BUCKET_NAME']

    @staticmethod
    def clear_temp_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    @classmethod
    def upload_to_s3(cls, file_path, file_key):
        s3 = S3Connector.get_conn()
        s3.meta.client.upload_file(file_path, cls.public_bucket_name, file_key, ExtraArgs={'ContentType': 'text/plain'})

        obj_acl = s3.ObjectAcl(cls.public_bucket_name, file_key)
        obj_acl.put(ACL='public-read')

    @classmethod
    def store_management_log(cls, file_path, suffix=''):
        try:
            file_path = str(file_path)
            file_key = f'management_log/{datetime.datetime.now().date()}_{uuid.uuid1().hex}{suffix}'

            cls.upload_to_s3(file_path, file_key)
            cls.clear_temp_file(file_path)

            return f'https://{cls.public_bucket_name}.s3.cn-north-1.amazonaws.com.cn/{file_key}'

        except:
            raise LogicError(f'保存失败！(err_msg){traceback.format_exc()}')

