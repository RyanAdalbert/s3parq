import boto3
import moto
import pytest
from core.constants import AWS_REGION
from core import dataset_contract
from dfmock import DFMock

@pytest.fixture
def df():
    columns = {"hamburger": "string",
               "bananas": "integer"
               }
    df = DFMock(count=100, columns=columns)
    yield df

@moto.mock.s3
@pytest.fixture
def bucket():
    bucket = "test-bucket"
    conn = boto3.resource('s3', region_name=AWS_REGION, aws_access_key_id="this_is_not_a_real_id",
                aws_secret_access_key="this_is_not_a_real_key")
    conn.create_bucket(Bucket=bucket)
    client = boto3.client('s3', region_name=AWS_REGION)
    yield bucket



@moto.mock.s3
def test_no_metadata(bucket):
    

@moto.mock.s3
def test_has_metadata(bucket):

@moto.mock.s3
def test_bad_run_id(bucket):