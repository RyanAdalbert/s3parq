from core.dataset_contract import DatasetContract
import core.helpers.contract_creator as contract_creator
import s3parq
import pandas as pd

class DatasetDiff():
    def __init__(self, transform_id: int):
        self.contract = contract_creator.contract_from_transformation_id(t_id=transform_id)
        return
    
    def get_diff(self, transform_name: str, partition="__metadata_run_id":str, part_vals:List[any], comparison="==":str)->pd.DataFrame:
        if not hasattr(self, 'contract') or type(self.contract) != DatasetContract:
            raise NameError("No source contract set. Did you pass a valid transform id when creating the class?")
        input_contract = contract_creator.get_relative_contract(t_name=transform_name, contract=self.contract)
        return s3parq.fetch(bucket=input_contract.bucket, key=input_contract.key, filters=[dict(partition=partition, comparison=comparison, values=part_vals)])

