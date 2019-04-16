import pytest
import dfmock 
import pandas as pd
from unittest.mock import patch
from core.contract import Contract
import boto3
import tempfile
from core.constants import ENVIRONMENT, ENV_BUCKET
import moto


@pytest.fixture
def _contract():
    contract = Contract(
            branch="master",
            parent="Merck",
            child="Wonder_Drug",
            state="ingest"
    )
    return contract


def test_set_env_valid(_contract):
    contract = _contract
    assert contract.env == f'{ENV_BUCKET}', 'failed to set to the current environment'

@patch("core.contract.ENVIRONMENT","Pretend-RSE")
def test_set_env_invalid():
    with pytest.raises(ValueError):
        contract = Contract(
            branch="master",
            parent="Merck",
            child="Wonder_Drug",
            state="ingest"
        )


def test_s3path(_contract):
    contract = _contract
    path = contract.s3_path

    assert path == f's3://{ENV_BUCKET}/master/merck/wonder_drug/ingest/', 'path was incorrectly built.'


def test_quick_set(_contract):
    contract = _contract

    assert contract.branch == 'master', 'failed to set branch'
    assert contract.env == f'{ENV_BUCKET}', 'failed to set env'
    assert contract.parent == 'merck', 'failed to set parent'
    assert contract.child == 'wonder_drug', 'failed to set child'
    assert contract.state == 'ingest', 'failed to set state'


def test_alias_brand(_contract):
    contract = _contract
    brand = 'Merck'
    contract.brand = brand
    assert contract.brand == brand.lower(), "brand alias not set"
    assert contract.child == brand.lower(), "brand does not alias to child"

def test_alias_customer(_contract):
    contract = _contract
    customer = 'Wonder_Drug'
    contract.customer = customer
    assert contract.customer == customer.lower(), "customer alias not set"
    assert contract.parent == customer.lower(), "customer does not alias to parent"

@pytest.fixture
def _contract_type():
    contract = Contract(branch='master',
                        parent='Merck',
                        child='Wonder_Drug',
                        state='ingest'
                        )
    return contract

def test_contract_type(_contract_type):
    contract = _contract_type
    assert contract.contract_type == 'state', 'returned wrong type for state contract'


def test_previous_state(_contract):
    contract = _contract
    contract.state = 'ingest'

    assert contract.previous_state == 'raw', 'previous state incorrect'


def test_previous_from_raw(_contract):
    contract = _contract
    contract.state = 'raw'
    assert contract.previous_state == None, 'previous state for raw'


def test_next_state(_contract):
    contract = _contract
    contract.state = 'ingest'
    assert contract.next_state == 'master', 'next state incorrect'


def test_next_state_from_dimensional(_contract):
    contract = _contract
    contract.state = 'dimensional'
    assert contract.next_state == None, 'next state for dimensinal'


def test_get_partition_size():
    contract = Contract()
    size = 1
    contract.set_partition_size(size)
    assert contract.get_partition_size() == size, 'partition size not correctly set'


def _s3_mock_setup():
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket=f'{ENV_BUCKET}')
    return s3_client


def _contract_setup():
    #contract = Contract()
    contract = Contract(branch='master',
                        parent='Merck',
                        child='Wonder_Drug',
                        state='raw'
                        )
    return contract


@moto.mock_s3()
def test_publish_raw_valid():
    client = _s3_mock_setup()
    contract = _contract_setup()
    # _s3_mock_setup()
    _file = tempfile.NamedTemporaryFile()
    text = b"Here's some money. Go see a Star War"
    _file.write(text)
    _file.seek(0)
    contract.publish_raw_file(_file.name)
    _file.close()

    key = f'master/merck/wonder_drug/raw/{os.path.split(_file.name)[1]}'
    s3_client = boto3.client('s3')
    body = s3_client.get_object(
        Bucket=f'{ENV_BUCKET}', Key=key)['Body'].read()
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

    with tempfile.NamedTemporaryFile() as _file:
        text = b"Here's some money. Go see a Star War"
        _file.write(text)
        _file.seek(0)
        contract.publish_raw_file(_file.name)
        f_time = os.stat(_file.name).st_mtime

        key = f'master/merck/wonder_drug/raw/{os.path.split(_file.name)[1]}'
        s3_client = boto3.client('s3')
        meta = s3_client.get_object(
            Bucket=f'{ENV_BUCKET}', Key=key)['Metadata']
        assert meta['source_modified_time'] == str(f_time)

def test_fetch_from_s3():
    with patch('core.contract.fetch', autospec=True) as fetch:
        fetch.return_value = pd.DataFrame()
        contract = Contract()
        contract.set_branch('master')
        contract.set_parent('Merck')
        contract.set_child('Wonder_Drug')
        contract.set_state('ingest')
        contract.set_dataset('valid_dataset')

        key = contract.get_key()
        filters = {"partition":"hamburger",
                    "comparison":"==",
                    "values":['McDonalds']}

        fake_df = contract.fetch(filters)

        fetch.assert_called_once_with(
            bucket=f'{ENV_BUCKET}',
            key=key,
            filters=filters)

        assert isinstance(fake_df, pd.DataFrame)

def test_publish_to_s3():
    with patch('core.contract.publish', autospec=True) as publish:
        df = dfmock.DFMock(count = 100, columns = {"fake":"boolean","partition":"string","option":{"option_count":4,"option_type":"string"}})
        df.generate_dataframe()
        patch.return_value = None
        contract = Contract()
        contract.set_branch('master')
        contract.set_parent('Merck')
        contract.set_child('Wonder_Drug')
        contract.set_state('ingest')
        contract.set_dataset('valid_dataset')

        key = contract.get_key()
        fake_parts = ["fake=True","partition=faker"]

        pub = contract.publish(dataframe=df.dataframe,partitions=fake_parts)

        publish.assert_called_once_with(
            bucket=f'{ENV_BUCKET}',
            dataframe=df.dataframe,
            key=key,
            partitions=fake_parts
            )
        assert pub is None

@moto.mock_s3()
def test_list_files():
    client = _s3_mock_setup()
    contract = _contract_setup()

    with tempfile.NamedTemporaryFile(prefix="imb4") as _file:
        text = b"Here's some money. Go see a Star War"
        _file.write(text)
        _file.seek(0)
        contract.publish_raw_file(_file.name)


        f_time = os.stat(_file.name).st_mtime
        key = f'master/merck/wonder_drug/raw/{os.path.split(_file.name)[1]}'

        files = contract.list_files('imb4')

        assert files == [key]
