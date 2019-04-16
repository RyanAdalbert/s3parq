import pytest
from unittest.mock import patch
from core.dataset_contract import DatasetContract
import boto3
from core.constants import ENVIRONMENT, ENV_BUCKET
import moto


@pytest.fixture
def _contract():
    contract = DatasetContract(
            branch="master",
            parent="Merck",
            child="Wonder_Drug",
            state="ingest",
            dataset="valid_dataset"
    )
    return contract


def test_dataset_only(_contract):
    contract = _contract
    path = contract.s3_path

    assert path == f's3://{ENV_BUCKET}/master/merck/wonder_drug/ingest/valid_dataset/', 'path was incorrectly built.'


def test_with_partitions(_contract):
    contract = _contract
    contract.partitions = ['partition_1', 'partition_2']
    path = contract.s3_path
    assert path == f's3://{ENV_BUCKET}/master/merck/wonder_drug/ingest/valid_dataset/', 'path was incorrectly built with partitions.'


def test_quick_set(_contract):
    contract = _contract

    assert contract.branch == 'master', 'failed to set branch'
    assert contract.env == f'{ENV_BUCKET}', 'failed to set env'
    assert contract.parent == 'merck', 'failed to set parent'
    assert contract.child == 'wonder_drug', 'failed to set parent'
    assert contract.state == 'ingest', 'failed to set parent'
    assert contract.dataset == 'valid_dataset', 'failed to set parent'


def test_valid_partitions(_contract):
    contract = _contract
    contract.partitions = ['date', 'segment']
    assert contract.partitions == ['date', 'segment'], "partitions not correctly set"


@pytest.fixture
def _contract_type():
    contract = DatasetContract(branch='master',
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


def test_get_partition_size():
    contract = _contract
    size = 1
    contract.partition_size = size
    assert contract.partition_size == size, 'partition size not correctly set'
