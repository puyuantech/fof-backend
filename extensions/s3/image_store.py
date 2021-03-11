
import os
import traceback
import uuid

from bases.exceptions import LogicError, VerifyError
from bases.globals import settings
from extensions.s3.s3_client import S3Connector


class ImageStore:

    store_path = settings['TEMP_PATH']
    private_bucket_name = settings['AWS_PRIVATE_BUCKET_NAME']

    @staticmethod
    def clear_temp_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def load_from_obj(file_obj, file_path):
        with open(file_path, 'wb') as f:
            f.write(file_obj.read())

    @classmethod
    def upload_to_s3(cls, file_path, file_key):
        s3 = S3Connector.get_conn()
        s3.meta.client.upload_file(file_path, cls.private_bucket_name, file_key, ExtraArgs={'ContentType': 'image/jpeg'})

        s3.ObjectAcl(cls.private_bucket_name, file_key)

    @classmethod
    def store_image_from_user(cls, user_id, file_obj, suffix=''):
        if not file_obj:
            raise VerifyError('上传失败！')

        try:
            image_id = uuid.uuid1().hex
            file_path = os.path.join(cls.store_path, f'image_from_user_{user_id}{suffix}')
            file_key = f'fof_image/{user_id}_{image_id}{suffix}'

            cls.load_from_obj(file_obj, file_path)
            cls.upload_to_s3(file_path, file_key)
            cls.clear_temp_file(file_path)

            # url: f'https://{cls.private_bucket_name}.s3.cn-northwest-1.amazonaws.com.cn/{file_key}'
            return file_key

        except:
            raise LogicError(f'保存失败！(err_msg){traceback.format_exc()}')

    @staticmethod
    def create_pre_signed_url(object_name, bucket_name=settings['AWS_PRIVATE_BUCKET_NAME'], expiration=3600):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        s3_client = S3Connector.get_client()
        return s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_name,
            },
            ExpiresIn=expiration
        )

