import pytest
import os
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
    yield contract


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


def test_contract_type(_contract):
    contract = _contract
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


def _s3_mock_setup():
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket=f'{ENV_BUCKET}')
    return s3_client

@moto.mock_s3()
def test_publish_raw_valid(_contract):
    client = _s3_mock_setup()
    contract = _contract
    contract.state = "raw"
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
def test_publish_raw_invalid(_contract):
    client = _s3_mock_setup()
    contract = _contract
    contract.state = 'enrich'

    _file = tempfile.NamedTemporaryFile()
    text = b"Here's some money. Go see a Star War"
    _file.write(text)
    _file.seek(0)

    with pytest.raises(ValueError):
        contract.publish_raw_file(_file.name)
    _file.close()


@moto.mock_s3()
def test_publish_raw_metadata(_contract):
    client = _s3_mock_setup()
    contract = _contract
    contract.state = "raw"
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



@moto.mock_s3()
def test_list_files(_contract):
    client = _s3_mock_setup()
    contract = _contract
    contract.state = 'raw'

    with tempfile.NamedTemporaryFile(prefix="imb4") as _file:
        text = b"Here's some money. Go see a Star War"
        _file.write(text)
        _file.seek(0)
        contract.publish_raw_file(_file.name)


        f_time = os.stat(_file.name).st_mtime
        key = f'master/merck/wonder_drug/raw/{os.path.split(_file.name)[1]}'

        files = contract.list_files('imb4')

        assert files == [key]
