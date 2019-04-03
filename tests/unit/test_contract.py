import pytest
from unittest.mock import patch
from core.contract import Contract
import boto3
import tempfile
from core.helpers.project_root import ProjectRoot
from core.constants import ENVIRONMENT, ENV_BUCKET
import moto
import os


@pytest.fixture
def _contract():
    contract = Contract(
            branch="master",
            parent="Merck",
            child="Wonder_Drug",
            state="ingest",
            dataset="valid_dataset"
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
            state="ingest",
            dataset="valid_dataset"
        )


def test_dataset_only(_contract):
    contract = _contract
    path = contract.s3_path

    assert path == f's3://{ENV_BUCKET}/master/merck/wonder_drug/ingest/valid_dataset/', 'path was incorrectly built.'


def test_with_partitions(_contract):
    contract = _contract
    contract.partitions = ['partition_1', 'partition_2']
    path = contract.s3_path
    assert path == f's3://{ENV_BUCKET}/master/merck/wonder_drug/ingest/valid_dataset/partition_1/partition_2/', 'path was incorrectly built with partitions.'


def test_quick_set(_contract):
    contract = _contract

    assert contract.branch == 'master', 'failed to set branch'
    assert contract.env == f'{ENV_BUCKET}', 'failed to set env'
    assert contract.parent == 'merck', 'failed to set parent'
    assert contract.child == 'wonder_drug', 'failed to set parent'
    assert contract.state == 'ingest', 'failed to set parent'
    assert contract.dataset == 'valid_dataset', 'failed to set parent'


def test_alias_brand(_contract):
    contract = _contract
    brand = 'Merck'
    contract.brand = brand
    assert contract.brand == brand.lower(), "brand alias not set"
    assert contract.child == brand.lower(), "brand does not alias to child"


@pytest.fixture
def _partitions():
    p = dict()
    p['good'] = ['date', 'segment']
    p['bad'] = ['b@d$$%Partition', 'good_partition_name']
    return p


def test_valid_partitions(_partitions, _contract):
    p = _partitions
    contract = _contract
    contract.partitions = p['good']
    assert contract.partitions == p['good'], "partitions not correctly set"


def test_invalid_partitions(_partitions, _contract):
    p = _partitions
    contract = _contract
    with pytest.raises(ValueError):
        contract.partitions = p['bad']


@pytest.fixture
def _contract_type():
    contract = Contract(branch='master',
                        parent='Merck',
                        child='Wonder_Drug',
                        state='ingest',
                        dataset="valid_dataset"
                        )
    return contract


def test_contract_type_state(_contract_type):
    contract = _contract_type
    assert contract.contract_type == 'dataset', 'returned wrong type for state contract'


def test_contract_type_dataset(_contract_type):
    contract = _contract_type
    contract.dataset = 'test_set'
    assert contract.contract_type == 'dataset', 'returned wrong type for dataset contract'


def test_contract_type_partitions(_contract_type):
    contract = _contract_type
    contract.partitions = ['test_par']
    assert contract.contract_type == 'partition', 'returned wrong type for partition contract'


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
    contract = _contract
    size = 1
    contract.partition_size = size
    assert contract.partition_size == size, 'partition size not correctly set'
