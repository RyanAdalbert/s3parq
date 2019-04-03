import pytest
from unittest.mock import patch
from core.transforms.shared.raw.raw_contract import RawContract
import boto3
import tempfile
from core.helpers.project_root import ProjectRoot
from core.constants import ENVIRONMENT, ENV_BUCKET
import moto
import os

def test_set_env_valid():
    contract = RawContract(
            parent="Merck",
            child="Wonder_Drug",
            state="raw"
        )
    assert contract.env == f'{ENV_BUCKET}', 'failed to set to the current environment'

@patch("core.transforms.shared.raw.raw_contract.ENVIRONMENT","Pretend-RSE")
def test_set_env_invalid():
    with pytest.raises(ValueError):
        contract = RawContract(
            parent="Merck",
            child="Wonder_Drug",
            state="raw"
        )


@pytest.fixture
def _contract():
    contract = RawContract(
        parent="Merck",
        child="Wonder_Drug",
        state="raw"
    )
    return contract


def test_alias_brand():
    contract = RawContract(
        parent="Merck",
        child="Wonder_Drug",
        state="raw"
    )
    brand = 'Merck'
    contract.brand = brand
    assert contract.brand == brand.lower(), "brand alias not set"
    assert contract.child == brand.lower(), "brand does not alias to child"


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
    contract.state = 'raw'
    assert contract.next_state == 'ingest', 'next state incorrect'


def test_next_state_from_ingest(_contract):
    contract = _contract
    contract.state = 'ingest'
    assert contract.next_state == None, 'next state for ingest'



def _s3_mock_setup():
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket=f'{ENV_BUCKET}')
    return s3_client


def _contract_setup():
    contract = RawContract(branch='master',
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
    contract.state = 'ingest'

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