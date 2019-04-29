from core.dataset_contract import DatasetContract
from core.helpers.session_helper import SessionHelper as SHelp
import core.helpers.contract_creator as contract_creator
import s3parq.fetch_parq as fetcher
import pandas as pd

class DatasetDiff():

    def __init__(self, transform_id: int):
        self.contract = contract_creator.contract_from_id(t_id=transform_id)
        return
    
    def get_diff(self, transform_name: str, partition="__metadata_run_timestamp")->pd.DataFrame:
        if not hasattr(self, 'contract'):
            raise NameError("Error: First transform not found!")
        delta = contract_creator.contract_from_name(t_name=transform_name, contract=self.contract)
        bucket = self.contract.bucket
        key = self.contract.key
        return fetcher.fetch_diff(input_bucket=bucket, input_key=key, comparison_bucket=delta.bucket, comparison_key=delta.key, partition=partition)
        