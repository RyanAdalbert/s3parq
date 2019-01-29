import pytest
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
import core.models.configuation as C
import core.contract as contract
from core.transforms.shared.raw.extract import ExtractTransform
import boto3
import moto
import time

'''
@moto.mock_s3
def setup_configs():
    ENV = "dev"
    mock = CMock()
    mock.generate_mocks()
    transform = C.Transformation()
    session = mock.get_session()
    t_target = session.query(transform).one()
    return  t_target

@moto.mock_s3
def setup_contract():
    ct = Contract(  env=ENV, 
                    parent = ,
                    child = ,
                    branch = ,
                    state = ,
                 )    
    return ct    



    ex = ExtractTransform(ENV, t_target,  
                            
'''
@moto.mock_s3
def s3_setup():
    client = boto3.client('s3')
    time = time.time()
    file_name = 'sandwiches12345.txt'
    BINARY_DATA = b'Gobias some coffee!'
    CONTRACT_PATH = f'master/bluth/cornballer/raw/{file_name}'
    client.create_bucket(Bucket= DEV_BUCKET)
    client.put_object(Body=BINARY_DATA, Bucket=BUCKET, Key= CONTRACT_PATH, ExtraArgs={"Metadata":{"source_modified_time": str(time - 10000000)}})
    return (file_name, time,)   


def test_push_to_s3_new_file():
    params = s3_setup()
    

def test_push_to_s3_updated_file():
    pass

def test_push_to_s3_not_if_older():
    pass

def test_file_needs_update_needs_update():
    pass

def test_file_needs_update_doesnt_need_update():
    pass

