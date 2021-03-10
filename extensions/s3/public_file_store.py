
import os
import traceback
import uuid
from bases.globals import settings
from extensions.s3.s3_client import S3Connector


class FileStore:
    def __init__(self):
        self.store_path = settings['TEMP_PATH']
        self.public_bucket_name = settings['AWS_PUBLIC_BUCKET_NAME']

    @classmethod
    def load_from_user(cls, file_obj, file_path):
        with open(file_path, 'wb') as f:
            f.write(file_obj.read())

    def upload_to_s3(self, file_path, file_key, content_type):
        s3 = S3Connector.get_conn()
        s3.meta.client.upload_file(file_path, self.public_bucket_name, file_key, ExtraArgs={'ContentType': content_type})

        obj_acl = s3.ObjectAcl(self.public_bucket_name, file_key)
        obj_acl.put(ACL='public-read')

    @staticmethod
    def clear_temp_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    def store_file_from_user(self, user_id, file_obj, content_type, suffix=''):
        if not file_obj or not self.public_bucket_name:
            return False, f'missing private_bucket_name (private_bucket_name){self.public_bucket_name}'

        try:
            image_id = uuid.uuid1().hex
            file_path = os.path.join(self.store_path, f'pdf_from_user_{user_id}{suffix}')
            file_key = f'fof_file/{user_id}_{image_id}{suffix}'

            self.load_from_user(file_obj, file_path)
            self.upload_to_s3(file_path, file_key, content_type)
            self.clear_temp_file(file_path)

            return file_key, f'https://{self.public_bucket_name}.s3.cn-north-1.amazonaws.com.cn/{file_key}'
        except:
            return False, traceback.format_exc()
