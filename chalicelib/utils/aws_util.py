from botocore.exceptions import ClientError
import boto3
import logging


def check_id_available(img_id, bucket, s3):
    try:
        s3.head_object(Bucket=bucket, Key=img_id)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            logging.debug('Not Found img_id' + str(img_id))
            logging.debug(e.response['Error']['Code'])
            return True
        else:
            raise e
    else:
        return False


