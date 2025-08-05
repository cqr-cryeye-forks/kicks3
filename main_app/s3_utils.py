# s3_utils.py

import boto3
import requests
import json
from .constants import HEADERS, TEST_FILE_CONTENT, TEST_FILE_NAME

def check_listings(bucket):
    unauth = False
    auth = False
    s3 = boto3.client('s3')
    try:
        session = requests.Session()
        response = session.get(f"http://{bucket}.s3.amazonaws.com", headers=HEADERS)
        if "<ListBucketResult xmlns" in response.text:
            unauth = True
        try:
            s3.list_objects(Bucket=bucket)
            auth = True
        except:
            pass
    except:
        pass
    return unauth, auth

def get_bucket_acl(bucket):
    try:
        s3 = boto3.client('s3')
        s3.get_bucket_acl(Bucket=bucket)
        return True
    except:
        return False

def put_bucket_policy(bucket):
    try:
        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Sid': 'AddPerm',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': 's3:*',
                'Resource': f'arn:aws:s3:::{bucket}/*'
            }]
        }
        s3 = boto3.client('s3')
        s3.put_bucket_policy(Bucket=bucket, Policy=json.dumps(bucket_policy))
        return True
    except:
        return False

def check_upload(bucket):
    try:
        s3 = boto3.resource('s3')
        s3.Object(bucket, TEST_FILE_NAME).put(Body=TEST_FILE_CONTENT)
        s3.ObjectAcl(bucket, TEST_FILE_NAME).put(ACL='public-read')
        return True
    except:
        return False