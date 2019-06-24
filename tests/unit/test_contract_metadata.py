import boto3
import moto
import pytest
from core.constants import AWS_REGION, ENV_BUCKET
from core.helpers import drop_metadata
from core import dataset_contract
from dfmock import DFMock
from unittest.mock import patch

@pytest.fixture
def contract():
    contract = dataset_contract.DatasetContract(parent="p", child="c", state="raw", dataset="test")
    yield contract

def test_no_metadata(contract): 
    with patch('s3parq.publish', autospec=True) as pub:
        columns = {"hamburger": "string",
                "bananas": "integer"}
        meta_cols = list(drop_metadata.get_meta_cols().keys())
        df = DFMock(count=100, columns=columns)
        df.generate_dataframe()
        df = df.dataframe
        for col in meta_cols:
            assert col not in df.columns
        contract._set_dataset_metadata(df=df, run_id=1)
        for col in meta_cols:
            assert col in df.columns
    
def test_has_metadata(contract): # don't overwrite __metadata cols if they exist
    columns = {"hamburger": "string",
               "bananas": "integer"}
    columns.update(drop_metadata.get_meta_cols())
    df = DFMock(count=50, columns=columns)
    df.generate_dataframe()
    df = df.dataframe
    id_col = df.loc[:, "__metadata_run_id"].copy()
    contract._set_dataset_metadata(df=df, run_id=1)
    assert df.loc[:, "__metadata_run_id"].all() == id_col.all()

def test_bad_run_id(contract):
    columns = {"hamburger": "string",
               "bananas": "integer"}
    df = DFMock(count=100, columns=columns)
    df.generate_dataframe()
    df = df.dataframe
    try:
        contract.publish(dataframe=df, run_id=24359)
        assert False
    except KeyError:
        assert True
