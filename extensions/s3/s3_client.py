import boto3
from bases.globals import settings


class S3Connector:

    @staticmethod
    def get_conn():
        return boto3.resource(
            's3',
            region_name=settings['AWS_REGION_NAME'],
            aws_access_key_id=settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=settings['AWS_SECRET_ACCESS_KEY'],
        )

    @staticmethod
    def get_client():
        return boto3.client(
            's3',
            region_name=settings['AWS_REGION_NAME'],
            aws_access_key_id=settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=settings['AWS_SECRET_ACCESS_KEY'],
        )


if __name__ == '__main__':

    from apps import create_app
    create_app().app_context().push()
    import boto3
    from botocore.exceptions import ClientError
    import requests


    def create_presigned_url(bucket_name, object_name, expiration=3600):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        s3_client = boto3.client(
            's3',
            region_name=settings['AWS_REGION_NAME'],
            aws_access_key_id=settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=settings['AWS_SECRET_ACCESS_KEY'],
        )
        try:
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': bucket_name,
                                                                'Key': object_name},
                                                        ExpiresIn=expiration)
        except ClientError as e:
            print(e)
            return None

        # The response contains the presigned URL
        return response

    url = create_presigned_url(settings['AWS_PRIVATE_BUCKET_NAME'], '1')
    print(url)
    if url is not None:
        'https://fof-private.s3.cn-north-1.amazonaws.com.cn/1?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAZQQJSZ6G3PJ6HROT%2F20210304%2Fcn-north-1%2Fs3%2Faws4_request&X-Amz-Date=20210304T043157Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=87fd3fe0ec59014c42618aa6bb3873863ae6d7acec7561290082a2cea5a1e4e9'
        'https://fof-private.s3.cn-north-1.amazonaws.com.cn/1?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAZQQJSZ6G3PJ6HROT%2F20210304%2Fcn-north-1%2Fs3%2Faws4_request&X-Amz-Date=20210304T043306Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=4be3d789f584c9a66e26dcbdaf6842f1309ddd8464ac092e8df1d7a060ffafbc'

        response = requests.get(url)
        print(response.content)
    # file_path = '/Users/puyuantech/Desktop/WechatIMG76.jpeg'
    # file_key = '1'
    #
    # s3 = S3Connector.get_conn()
    # s3.meta.client.upload_file(file_path, settings['AWS_PRIVATE_BUCKET_NAME'], file_key, ExtraArgs={'ContentType': 'image/jpeg'})
    #
    # obj_acl = s3.ObjectAcl(['AWS_PRIVATE_BUCKET_NAME'], file_key)

