import os
import boto3
from botocore.exceptions import ClientError

from app.logger.logger import logger

def generate_presigned_url(s3_url:str, expiration:int=3600):
    """
    Generate a presigned URL for an S3 object.

    :param s3_url: The S3 URL of the object
    :param expiration: The number of seconds the presigned URL is valid for (default is 1 hour)
    :return: Presigned URL as string. If error, returns None.
    """
    try:
        parts = s3_url.split('/')
        bucket_name = parts[2].split('.')[0]
        key = '/'.join(parts[3:])
    except IndexError:
        print("Invalid S3 URL format")
        return None

    # Create a boto3 client
    s3_client = boto3.client(
        's3',
        region_name=os.environ.get('AWS_REGION','eu-west-1')
    )

    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': key},
                                                    ExpiresIn=expiration)
        return response
    except ClientError as e:
        logger.error(f"Error generating presigned URL: {e}",exc_info= True)
        raise e

