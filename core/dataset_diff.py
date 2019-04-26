from core.dataset_contract import DatasetContract as DSContract
from core.helpers.session_helper import SessionHelper as SHelp
from s3parq import fetch_diff
import pandas as pd

def contract_from_id(transform_id: int):
    pass

class DatasetDiff():

    def __init__(self, transform_id: int):
        pass
    
    def get_diff(self, transform_id: int)->pd.DataFrame:
        pass