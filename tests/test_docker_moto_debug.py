import pytest
import os

import boto3
import moto 

@moto.mock_s3
def test_all_the_things():
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='mybucket')
    client = boto3.client('s3', region_name='us-east-1')
    client.put_object(Bucket='mybucket', Key='banana', Body='body stuff!')
    
    body = conn.Object('mybucket', 'banana').get()['Body'].read().decode("utf-8")

    assert body == 'body stuff!'

