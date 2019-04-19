import pytest
from unittest.mock import patch
from core.dataset_contract import DatasetContract
import boto3
from core.constants import ENVIRONMENT, ENV_BUCKET
import pandas as pd
import dfmock
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
    assert path == f's3://{ENV_BUCKET}/master/merck/wonder_drug/ingest/valid_dataset/partition_1/partition_2/', 'path was incorrectly built with partitions.'


def test_quick_set(_contract):
    contract = _contract

    assert contract.branch == 'master', 'failed to set branch'
    assert contract.env == f'{ENV_BUCKET}', 'failed to set env'
    assert contract.parent == 'merck', 'failed to set parent'
    assert contract.child == 'wonder_drug', 'failed to set parent'
    assert contract.state == 'ingest', 'failed to set parent'
    assert contract.dataset == 'valid_dataset', 'failed to set parent'


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


def test_fetch_from_s3(_contract):
    with patch('core.contract.fetch', autospec=True) as fetch:
        fetch.return_value = pd.DataFrame()
        contract = _contract
        contract.branch = 'master'
        contract.parent ='Merck'
        contract.child = 'Wonder_Drug'
        contract.state = 'ingest'
        contract.dataset = 'valid_dataset'

        key = contract.key
        filters = {"partition":"hamburger",
                    "comparison":"==",
                    "values":['McDonalds']}

        fake_df = contract.fetch(filters)

        fetch.assert_called_once_with(
            bucket=f'{ENV_BUCKET}',
            key=key,
            filters=filters)

        assert isinstance(fake_df, pd.DataFrame)

def test_publish_to_s3(_contract):
    with patch('core.contract.publish', autospec=True) as publish:
        df = dfmock.DFMock(count = 100, columns = {"fake":"boolean","partition":"string","option":{"option_count":4,"option_type":"string"}})
        df.generate_dataframe()
        patch.return_value = None
        contract = _contract
        contract.branch = 'master'
        contract.parent = 'Merck'
        contract.child = 'Wonder_Drug'
        contract.state = 'ingest'
        contract.dataset = 'valid_dataset'

        key = contract.key
        fake_parts = ["fake=True","partition=faker"]

        pub = contract.publish(dataframe=df.dataframe,partitions=fake_parts)

        publish.assert_called_once_with(
            bucket=f'{ENV_BUCKET}',
            dataframe=df.dataframe,
            key=key,
            partitions=fake_parts
            )
        assert pub is None
