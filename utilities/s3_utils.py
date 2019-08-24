import logging
import os
import boto3
from botocore.exceptions import ClientError


def put_object(dest_bucket_name, dest_object_name, object_content):

    # Put the object
    s3 = boto3.client(
        's3', 
        aws_access_key_id='INSERT_ACCESS_KEY_ID', 
        aws_secret_access_key='INSERT_SECRET_ACCESS_KEY')

    try:
        s3.put_object(Bucket=dest_bucket_name, Key=dest_object_name, Body=object_content)
    except ClientError as e:
        # AllAccessDisabled error == bucket not found
        # NoSuchKey or InvalidRequest error == (dest bucket/obj == src bucket/obj)
        print(f"An error occurred uploading to S3: {e}")
        return False
    return True