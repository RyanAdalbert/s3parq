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
    output_contract = contract.Contract(branch='master', parent='bluth', child='cornballer',state='raw',env='dev')
    client.create_bucket(Bucket= DEV_BUCKET)

    t_file_old = tempfile.NamedTemporaryFile()
    t_file_old.write(b'Gobias some old coffee!')
    file_name_old = os.path.split(t_file_old.name)[1]
    output_contract.set_file_name(file_name_old)
    client.upload_file(Bucket=DEV_BUCKET, Filename= t_file_old.name, Key= output_contract.get_key(), ExtraArgs={"Metadata":{"source_modified_time": str(n_time - time_delta)}})
    
    t_file_new = tempfile.NamedTemporaryFile()
    t_file_new.write(b'Gobias some new coffee!')
    file_name_new = os.path.split(t_file_new.name)[1]
    output_contract.set_file_name(file_name_new)
    client.upload_file(Bucket=DEV_BUCKET, Filename= t_file_new.name, Key= output_contract.get_key(), ExtraArgs={"Metadata":{"source_modified_time": str(n_time + time_delta)}})
    
    return (t_file_old, t_file_new, output_contract, time_delta)

@moto.mock_s3
def test_push_to_s3_updated_file():
    params = s3_setup()
    extract = ExtractTransform()
    client = boto3.client('s3')
    extract.push_to_s3(tmp_dir=os.path.dirname(params[0].name),
                       output_contract=params[2])
    params[2].set_file_name(os.path.split(params[0].name)[1])
    s3_time = float(client.head_object(Bucket=DEV_BUCKET, Key=params[2].get_key())['Metadata']['source_modified_time'])
    
    assert os.stat(params[0].name).st_mtime == s3_time             

@moto.mock_s3
def test_push_to_s3_new_file():
    params = s3_setup()
    extract = ExtractTransform()
    client = boto3.client('s3')
    t_file = tempfile.NamedTemporaryFile()
    t_file.write(b'Gobias some fresh coffee!')
    extract.push_to_s3(tmp_dir=os.path.dirname(t_file.name),
                    output_contract=params[2])
    params[2].set_file_name(os.path.split(t_file.name)[1])
    s3_time = float(client.head_object(Bucket=DEV_BUCKET, Key=params[2].get_key())['Metadata']['source_modified_time'])
    
    assert os.stat(t_file.name).st_mtime == s3_time

@moto.mock_s3
def test_push_to_s3_not_if_older():
    params = s3_setup()
    extract = ExtractTransform()
    client = boto3.client('s3')
    params[2].set_file_name(os.path.split(params[1].name)[1])
    s3_time_before = float(client.head_object(Bucket=DEV_BUCKET, Key=params[2].get_key())['Metadata']['source_modified_time'])
    extract.push_to_s3(tmp_dir=os.path.dirname(params[1].name),
                       output_contract=params[2])
    params[2].set_file_name(os.path.split(params[1].name)[1])
    s3_time_after = float(client.head_object(Bucket=DEV_BUCKET, Key=params[2].get_key())['Metadata']['source_modified_time'])
    
    assert s3_time_after == s3_time_before

@moto.mock_s3
def test_file_needs_update_needs_update():
    params = s3_setup()
    extract = ExtractTransform()
    check_update = extract._file_needs_update(params[2], params[0].name, os.stat(params[0].name).st_mtime)
    assert check_update == True

@moto.mock_s3
def test_file_needs_update_doesnt_need_update():
    params = s3_setup()
    extract = ExtractTransform()
    check_update = extract._file_needs_update(params[2], params[1].name, 0)
    assert check_update == False

@moto.mock_s3
def test_file_needs_update_doesnt_exist():
    params = s3_setup()
    extract = ExtractTransform()
    t_file = tempfile.NamedTemporaryFile()
    t_file.write(b'Gobias some coffee!')
    check_update = extract._file_needs_update(params[2], t_file, os.stat(t_file.name).st_mtime)
    assert check_update == True

def test_extract_validate_params_bad():
    with pytest.raises(ValueError) as e:
        output_contract = contract.Contract(branch='master', parent='bluth', child='cornballer',state='raw',env='dev')
        extract = ExtractTransform(env="not-an-env",output_contract=output_contract)
        extract._validate_required_params()

    assert e.type == ValueError

def test_extract_validate_params_good():
    output_contract = contract.Contract(branch='master', parent='bluth', child='cornballer',state='raw',env='dev')
    transformation = C.Transformation()
    extract = ExtractTransform(env="dev",output_contract=output_contract,transform=transformation)
    extract._validate_required_params()

def test_set_env_good():
    extract =  ExtractTransform()
    extract.set_env("dev")

    assert extract.env == "dev"

def test_set_env_bad():
    with pytest.raises(ValueError) as e:
        extract = ExtractTransform()
        extract.set_env("not-an-env")

    assert e.type == ValueError

def test_set_output_contract():
    output_contract = contract.Contract(branch='master', parent='bluth', child='cornballer',state='raw',env='dev')
    extract = ExtractTransform()
    extract.set_output_contract(output_contract)

    assert output_contract == extract.output_contract

def test_set_transform():
    transformation = C.Transformation()
    extract = ExtractTransform()
    extract.set_transform(transformation)

    assert transformation == extract.transform