import boto3
from ..core.config import settings
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

def upload_to_s3(file_data: bytes, key: str) -> str:
    try:
        s3_client.put_object(
            Bucket=settings.S3_BUCKET,
            Key=key,
            Body=file_data
        )
        return f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
    except ClientError as e:
        logger.error(f"Error uploading to S3: {e}")
        return ""

def get_s3_url(key: str) -> str:
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.S3_BUCKET,
                'Key': key
            },
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return url
    except ClientError as e:
        logger.error(f"Error generating S3 URL: {e}")
        return ""

def delete_from_s3(key: str) -> bool:
    try:
        s3_client.delete_object(
            Bucket=settings.S3_BUCKET,
            Key=key
        )
        return True
    except ClientError as e:
        logger.error(f"Error deleting from S3: {e}")
        return False 