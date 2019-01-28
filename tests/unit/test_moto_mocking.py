'''IS MOTO WORKING?!?!?
    Moto is a little finicky, so this test is to confirm:
    - moto is actually working for a given API
    - calls are not actually hitting real AWS!
    before you spend hours debugging your actual unit tests. 
'''
import boto3
import moto
import pytest
from core.constants import AWS_REGION

@moto.mock_s3
def test_s3_is_working():
    conn = boto3.resource('s3', region_name=AWS_REGION, aws_access_key_id="this_is_not_a_real_id",
                          aws_secret_access_key="this_is_not_a_real_key")
    conn.create_bucket(Bucket='mybucket')
    client = boto3.client('s3', region_name=AWS_REGION)
    client.put_object(Bucket='mybucket', Key='banana', Body='body stuff!')

    body = conn.Object('mybucket', 'banana').get()[
        'Body'].read().decode("utf-8")

    assert body == 'body stuff!'


@moto.mock_secretsmanager
def test_secretsmanager_is_working():
    conn = boto3.client('secretsmanager', region_name=AWS_REGION,
                        aws_access_key_id="this_is_not_a_real_id", aws_secret_access_key="this_is_not_a_real_key")
    conn.create_secret(Name='test_hamburger', SecretString='string')
