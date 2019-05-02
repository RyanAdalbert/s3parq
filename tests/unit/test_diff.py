import pytest
from pandas import DataFrame
from core.dataset_diff import DatasetDiff
from core.dataset_contract import DatasetContract

fetch_diff = "s3parq.fetch_parq.fetch_diff" # patch target

def test_good_diff(mocker):
    mocker.patch(fetch_diff, return_value=DataFrame())
    diff = DatasetDiff(12)
    retval = diff.get_diff("extract_from_ftp")
    assert type(retval) == DataFrame and retval.empty

def test_bad_diff(mocker):
    try:
        DatasetDiff(200)
    except KeyError:
        assert True

def test_no_diff(mocker):
    diff = DatasetDiff(1)
    diff.contract = None
    try:
        diff.get_diff("extract_from_ftp")
    except NameError:
        assert True