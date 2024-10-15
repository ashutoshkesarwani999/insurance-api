import os
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

from app.logger.logger import logger


aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")


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
    try:
        s3_client = boto3.client(
        's3',
        region_name=os.environ.get('AWS_REGION','eu-west-1'),
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    except (NoCredentialsError, PartialCredentialsError) as e:
        logger.error(f"Error in AWS credentials: {e}",exc_info=True)
        raise e
    except Exception as e:
        logger.error(f"An error occurred while creating the S3 client: {e}",exc_info=True)
        raise e

    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': key},
                                                    ExpiresIn=expiration)
        return response
    except ClientError as e:
        logger.error(f"Error generating presigned URL: {e}",exc_info= True)
        raise e

