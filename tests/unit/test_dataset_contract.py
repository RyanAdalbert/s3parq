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
        branch="fine-feature-branch",
        parent="Merck",
        child="Wonder_Drug",
        state="ingest",
        dataset="valid_dataset"
    )
    return contract


def test_dataset_only(_contract):
    contract = _contract
    path = contract.s3_path

    assert path == f's3://{ENV_BUCKET}/fine-feature-branch/merck/wonder_drug/ingest/valid_dataset', 'path was incorrectly built.'


def test_with_partitions(_contract):
    contract = _contract
    contract.partitions = ['partition_1', 'partition_2']
    path = contract.s3_path
    assert path == f's3://{ENV_BUCKET}/fine-feature-branch/merck/wonder_drug/ingest/valid_dataset', 'path was incorrectly built with partitions.'


def test_quick_set(_contract):
    contract = _contract

    assert contract.branch == 'fine-feature-branch', 'failed to set branch'
    assert contract.env == f'{ENV_BUCKET}', 'failed to set env'
    assert contract.parent == 'merck', 'failed to set parent'
    assert contract.child == 'wonder_drug', 'failed to set parent'
    assert contract.state == 'ingest', 'failed to set parent'
    assert contract.dataset == 'valid_dataset', 'failed to set parent'


def test_valid_partitions(_contract):
    contract = _contract
    contract.partitions = ['date', 'segment']
    assert contract.partitions == [
        'date', 'segment'], "partitions not correctly set"


@pytest.fixture
def _contract_type():
    contract = DatasetContract(branch='fine-feature-branch',
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


def test_get_partition_size():
    contract = _contract
    size = 1
    contract.partition_size = size
    assert contract.partition_size == size, 'partition size not correctly set'


def test_fetch_from_s3(_contract):
    with patch('core.dataset_contract.fetch', autospec=True) as fetch:
        fetch.return_value = pd.DataFrame()
        contract = _contract
        contract.branch = 'fine-feature-branch'
        contract.parent ='Merck'
        contract.child = 'Wonder_Drug'
        contract.state = 'ingest'
        contract.dataset = 'valid_dataset'

        key = contract.key
        filters = [{"partition": "hamburger",
                    "comparison": "==",
                    "values": ['McDonalds']}]

        fake_df = contract.fetch(filters)

        fetch.assert_called_once_with(
            bucket=f'{ENV_BUCKET}',
            key=key,
            filters=filters)

        assert isinstance(fake_df, pd.DataFrame)


def test_publish_to_s3(_contract):
    with patch('core.dataset_contract.publish', autospec=True) as publish:
        df = dfmock.DFMock(count=100, columns={"fake": "boolean", "partition": "string", "option": {
                           "option_count": 4, "option_type": "string"}})
        df.generate_dataframe()
        patch.return_value = None
        contract = _contract
        contract.branch = 'fine-feature-branch'
        contract.parent = 'Merck'
        contract.child = 'Wonder_Drug'
        contract.state = 'ingest'
        contract.dataset = 'valid_dataset'

        key = contract.key
        fake_parts = ["fake", "option"]
        contract.partitions = fake_parts

        pub = contract.publish(dataframe=df.dataframe)

        publish.assert_called_once_with(
            bucket=f'{ENV_BUCKET}',
            dataframe=df.dataframe,
            key=key,
            partitions=fake_parts
        )
        assert pub is None
