from core.dataset_contract import DatasetContract
from core.helpers.session_helper import SessionHelper as SHelp
from core.models.configuration import TransformationTemplate
import core.helpers.contract_creator as contract_creator
import s3parq.fetch_parq as fetcher
import pandas as pd

class DatasetDiff():
    def __init__(self, transform_id: int):
        self.contract = contract_creator.contract_from_transformation_id(t_id=transform_id)
        return
    
    def get_diff(self, transform_name: str, partition="__metadata_run_timestamp")->pd.DataFrame:
        if not hasattr(self, 'contract') or type(self.contract) != DatasetContract:
            raise NameError("No source contract set. Did you pass a valid transform id when creating the class?")
        delta = contract_creator.get_relative_contract(t_name=transform_name, contract=self.contract)
        bucket = self.contract.bucket
        key = self.contract.key
        print(bucket, key, delta.bucket, delta.key, partition)
        return fetcher.fetch_diff(input_bucket=delta.bucket, input_key=delta.key, comparison_bucket=bucket, comparison_key=key, partition=partition)
        