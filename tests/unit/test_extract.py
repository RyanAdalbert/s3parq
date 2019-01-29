import pytest
from core.constants import DEV_BUCKET
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
import core.models.configuration as C
import core.contract as contract
from core.transforms.shared.raw.extract import ExtractTransform
import boto3
import moto
import time
import tempfile
import os

@moto.mock_s3
def s3_setup():
    client = boto3.client('s3')
    n_time = time.time()
    time_delta = 10000000
    t_file = tempfile.NamedTemporaryFile()
    t_file.write(b'Gobias some coffee!')
    file_name = os.path.split(t_file.name)[1]
    output_contract = contract.Contract(branch='master', parent='bluth', child='cornballer',state='raw',env='dev', file_name = file_name)
    client.create_bucket(Bucket= DEV_BUCKET)
    client.upload_file(Bucket=DEV_BUCKET, Filename= t_file.name, Key= output_contract.get_key(), ExtraArgs={"Metadata":{"source_modified_time": str(n_time - time_delta)}})
    return (t_file, output_contract, time, time_delta)   


def test_push_to_s3_updated_file():
    params = s3_setup()
    extract = ExtractTransform()
    extract.push_to_s3(tmp_dir=os.path.dirname(params[0].name),
                       output_contract=params[1])
    client = boto3.client('s3')
    s3_time = float(client.head_object(Bucket=DEV_BUCKET, Key=Contract.get_key())['Metadata']['source_modified_time'])
    
    assert os.stat(t_file.name).st_mtime == s3_time                    

def test_push_to_s3_new_file():
    pass

def test_push_to_s3_not_if_older():
    pass

def test_file_needs_update_needs_update():
    pass

def test_file_needs_update_doesnt_need_update():
    pass

