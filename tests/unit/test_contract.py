import pytest
from core.contract import Contract
import boto3
import tempfile
from core.helpers.project_root import ProjectRoot
from core.constants import DEV_BUCKET
import moto
import os


def test_set_env_valid():
    contract = Contract()
    contract.set_env('dev')
    assert contract.env == f'{DEV_BUCKET}', 'failed to set dev environment'


def test_set_env_invalid():
    contract = Contract()

    with pytest.raises(ValueError):
        contract.set_env('Merck')


def test_get_s3_path_not_empty():
    contract = Contract()
    with pytest.raises(ValueError):
        contract.get_s3_path()


@pytest.fixture
def _contract():
    contract = Contract()
    contract.set_branch('master')
    contract.set_env('dev')
    contract.set_parent('Merck')
    contract.set_child('Wonder_Drug')
    contract.set_state('ingest')
    contract.set_dataset('valid_dataset')
    return contract


def test_dataset_only(_contract):
    contract = _contract
    path = contract.get_s3_path()

    assert path == f's3://{DEV_BUCKET}/master/merck/wonder_drug/ingest/valid_dataset/', 'path was incorrectly built.'


def test_with_partitions(_contract):
    contract = _contract
    contract.set_partitions(['partition_1', 'partition_2'])
    path = contract.get_s3_path()
    assert path == f's3://{DEV_BUCKET}/master/merck/wonder_drug/ingest/valid_dataset/partition_1/partition_2/', 'path was incorrectly built with partitions.'


def test_with_file_name_with_partitions(_contract):
    contract = _contract
    contract.set_file_name('29980385023509.parquet')
    contract.set_partitions(['partition_1', 'partition_2'])
    path = contract.get_s3_path()
    assert path == f's3://{DEV_BUCKET}/master/merck/wonder_drug/ingest/valid_dataset/partition_1/partition_2/29980385023509.parquet', 'path was incorrectly built with partitions.'


def test_file_name_no_partitions(_contract):
    contract = _contract
    contract.partitions = []  # hack to jump around the 0 len guard
    contract.set_file_name('29980385023509.parquet')
    path = contract.get_s3_path()
    assert path == f's3://{DEV_BUCKET}/master/merck/wonder_drug/ingest/valid_dataset/29980385023509.parquet', 'path was incorrectly built without partitions and with file name.'


def test_quick_set(_contract):
    contract = _contract
    contract = Contract(branch='master',
                        env='dev',
                        parent='Merck',
                        child='Wonder_Drug',
                        state='ingest',
                        dataset='valid_dataset')

    assert contract.get_branch() == 'master', 'failed to set branch'
    assert contract.get_env() == f'{DEV_BUCKET}', 'failed to set env'
    assert contract.get_parent() == 'merck', 'failed to set parent'
    assert contract.get_child() == 'wonder_drug', 'failed to set parent'
    assert contract.get_state() == 'ingest', 'failed to set parent'
    assert contract.get_dataset() == 'valid_dataset', 'failed to set parent'


def test_alias_brand():
    contract = Contract()
    brand = 'Merck'
    contract.set_brand(brand)
    assert contract.get_brand() == brand.lower(), "brand alias not set"
    assert contract.get_child() == brand.lower(), "brand does not alias to child"


@pytest.fixture
def _partitions():
    p = dict()
    p['good'] = ['date', 'segment']
    p['bad'] = ['b@d$$%Partition', 'good_partition_name']
    return p


def test_valid_partitions(_partitions):
    p = _partitions
    contract = Contract()
    contract.set_partitions(p['good'])
    assert contract.get_partitions(
    ) == p['good'], "partitions not correctly set"


def test_invalid_partitions(_partitions):
    p = _partitions
    contract = Contract()
    with pytest.raises(ValueError):
        contract.set_partitions(p['bad'])


@pytest.fixture
def _file_names():
    good_file_name = '23598020358908325.parquet'
    bad_file_name = '@@$10-8953095830-.jpg'
    return {'good': good_file_name, 'bad': bad_file_name}


def test_set_valid_file_name(_file_names):
    f = _file_names
    contract = Contract()
    contract.set_file_name(f['good'])
    assert contract.get_file_name() == f['good'], "file name was not set"


def test_set_invalid_file_name(_file_names):
    f = _file_names
    contract = Contract()
    with pytest.raises(ValueError):
        contract.set_file_name(f['bad'])


@pytest.fixture
def _contract_type():
    contract = Contract(branch='master',
                        env='dev',
                        parent='Merck',
                        child='Wonder_Drug',
                        state='ingest'
                        )
    return contract


def test_contract_type_state(_contract_type):
    contract = _contract_type
    assert contract.get_contract_type() == 'state', 'returned wrong type for state contract'


def test_contract_type_dataset(_contract_type):
    contract = _contract_type
    contract.set_dataset('test_set')
    assert contract.get_contract_type(
    ) == 'dataset', 'returned wrong type for dataset contract'


def test_contract_type_partitions(_contract_type):
    contract = _contract_type
    contract.set_partitions(['test_par'])
    assert contract.get_contract_type(
    ) == 'partition', 'returned wrong type for partition contract'


def test_contract_type_file(_contract_type):
    contract = _contract_type
    contract.set_partitions(['test_par'])
    contract.set_file_name('test_file.jpg')
    assert contract.get_contract_type() == 'file', 'returned wrong type for file contract'


def test_contract_type_file_no_partition(_contract_type):
    contract = _contract_type
    contract.partitions = []
    contract.set_file_name('test_file.jpg')
    assert contract.get_contract_type(
    ) == 'file', 'returned wrong type for file contract without partition'


def test_previous_state(_contract):
    contract = _contract
    contract.set_state('ingest')

    assert contract.get_previous_state() == 'raw', 'previous state incorrect'


def test_previous_from_raw(_contract):
    contract = _contract
    contract.set_state('raw')
    assert contract.get_previous_state() == None, 'previous state for raw'


def test_next_state(_contract):
    contract = _contract
    contract.set_state('ingest')
    assert contract.get_next_state() == 'master', 'next state incorrect'


def test_next_state_from_dimensional(_contract):
    contract = _contract
    contract.set_state('dimensional')
    assert contract.get_next_state() == None, 'next state for dimensinal'


def test_get_partition_size():
    contract = Contract()
    size = 1
    contract.set_partition_size(size)
    assert contract.get_partition_size() == size, 'partition size not correctly set'


def _s3_mock_setup():
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket=f'{DEV_BUCKET}')
    return s3_client

def _contract_setup():
    contract = Contract()
    contract = Contract(branch='master',
                        env='dev',
                        parent='Merck',
                        child='Wonder_Drug',
                        state='raw'
                        )
    return contract

@moto.mock_s3()
def test_publish_raw_valid():
    client = _s3_mock_setup()
    contract = _contract_setup()
    #_s3_mock_setup()
    _file = tempfile.NamedTemporaryFile()
    text = b"Here's some money. Go see a Star War"
    _file.write(text)
    _file.seek(0)
    contract.publish_raw_file(_file.name)
    _file.close()

    key = f'master/merck/wonder_drug/raw/{os.path.split(_file.name)[1]}'
    s3_client = boto3.client('s3')
    body = s3_client.get_object(
        Bucket=f'{DEV_BUCKET}', Key=key)['Body'].read()
    assert body == text

@moto.mock_s3()
def test_publish_raw_invalid():
    client = _s3_mock_setup()
    contract = _contract_setup()
    contract.set_state('enrich')

    _file = tempfile.NamedTemporaryFile()
    text = b"Here's some money. Go see a Star War"
    _file.write(text)
    _file.seek(0)

    with pytest.raises(ValueError):
        contract.publish_raw_file(_file.name)
    _file.close()

@moto.mock_s3()
def test_publish_raw_metadata():
    client = _s3_mock_setup()
    contract = _contract_setup()

    _file = tempfile.NamedTemporaryFile()
    text = b"Here's some money. Go see a Star War"
    _file.write(text)
    f_time = os.stat(_file.name).st_mtime
    _file.seek(0)
    contract.publish_raw_file(_file.name)
    _file.close()

    key = f'master/merck/wonder_drug/raw/{os.path.split(_file.name)[1]}'
    s3_client = boto3.client('s3')
    meta = s3_client.get_object(
        Bucket=f'{DEV_BUCKET}', Key=key)['Metadata']
    assert meta['source_modified_time'] == str(f_time)
