import pytest
from core.helpers.dataset_diff import DatasetDiff
from core.dataset_contract import DatasetContract

fetch_diff = "s3parq.fetch_parq.fetch_diff" # patch target
c_from_name = "core.helpers.contract_creator.contract_from_name"

def test_good_diff(mocker):
    mocker.patch("s3parq.fetch_parq.fetch_diff", return_value="lmao")
    diff = DatasetDiff(12)
    test = diff.get_diff("extract_from_ftp")
    raise ValueError(test)

def test_bad_diff(mocker):
    try:
        diff = DatasetDiff(200)
    except KeyError:
        assert True