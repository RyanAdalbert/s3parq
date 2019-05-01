from core.dataset_contract import DatasetContract
from core.helpers.session_helper import SessionHelper as SHelp
from core.models.configuration import TransformationTemplate
import core.helpers.contract_creator as contract_creator
import s3parq.fetch_parq as fetcher
import pandas as pd

# The parent/child info for the returned contract is populated from an extant contract, typically the one used to construct DatasetDiff.
def _contract_from_dataset_name(t_name: str, contract:DatasetContract)->DatasetContract:
    sess = SHelp().session
    template = sess.query(TransformationTemplate).filter(TransformationTemplate.name==t_name).first()
    if template is None:
        raise KeyError("Error: No transform found with name " + t_name)
    dataset = template.name
    state = template.pipeline_state_type.name 
    return DatasetContract(parent=contract.parent, child=contract.child, state=state, dataset=dataset) 

class DatasetDiff():
    def __init__(self, transform_id: int):
        self.contract = contract_creator.contract_from_transformation_id(t_id=transform_id)
        return
    
    def get_diff(self, transform_name: str, partition="__metadata_run_timestamp")->pd.DataFrame:
        if not hasattr(self, 'contract') or type(self.contract) != DatasetContract:
            raise NameError("No source contract set. Did you pass a valid transform id when creating the class?")
        delta = _contract_from_dataset_name(t_name=transform_name, contract=self.contract)
        bucket = self.contract.bucket
        key = self.contract.key
        return fetcher.fetch_diff(input_bucket=bucket, input_key=key, comparison_bucket=delta.bucket, comparison_key=delta.key, partition=partition)
        