
import os
import traceback
import uuid
from botocore.exceptions import ClientError
from bases.globals import settings
from extensions.s3.s3_client import S3Connector


class PdfStore:
    def __init__(self):
        self.store_path = settings['TEMP_PATH']
        self.private_bucket_name = settings['AWS_PRIVATE_BUCKET_NAME']

    @classmethod
    def load_from_user(cls, file_obj, file_path):
        with open(file_path, 'wb') as f:
            f.write(file_obj.read())

    def upload_to_s3(self, file_path, file_key):
        s3 = S3Connector.get_conn()
        s3.meta.client.upload_file(file_path, self.private_bucket_name, file_key, ExtraArgs={'ContentType': 'application/pdf'})

        s3.ObjectAcl(self.private_bucket_name, file_key)

    @staticmethod
    def clear_temp_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    def store_pdf_from_user(self, user_id, file_obj, suffix=''):
        if not file_obj or not self.private_bucket_name:
            return False, f'missing private_bucket_name (private_bucket_name){self.private_bucket_name}'

        try:
            image_id = uuid.uuid1().hex
            file_path = os.path.join(self.store_path, f'pdf_from_user_{user_id}{suffix}')
            file_key = f'fof_info/{user_id}_{image_id}{suffix}'

            self.load_from_user(file_obj, file_path)
            self.upload_to_s3(file_path, file_key)
            self.clear_temp_file(file_path)

            return file_key, f'https://{self.private_bucket_name}.s3.cn-northwest-1.amazonaws.com.cn/{file_key}'

        except:
            return False, traceback.format_exc()

    def create_pre_signed_url(self,  object_name, bucket_name=settings['AWS_PRIVATE_BUCKET_NAME'], expiration=3600):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        s3_client = S3Connector.get_client()
        try:
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': bucket_name,
                                                                'Key': object_name},
                                                        ExpiresIn=expiration)
        except ClientError as e:
            print(e)
            return False, traceback.format_exc()

        # The response contains the presigned URL
        return response

