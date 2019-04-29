from core.dataset_contract import DatasetContract as DSContract
from core.helpers.session_helper import SessionHelper as SHelp
from core.constants import ENVIRONMENT, DEV_BUCKET, PROD_BUCKET, UAT_BUCKET, BRANCH_NAME
from s3parq import fetch_diff
import pandas as pd

def _contract_from_id(transform_id: int):
    pass

class DatasetDiff():
    DEV = DEV_BUCKET
    PROD = PROD_BUCKET
    UAT = UAT_BUCKET

    def __init__(self, transform_id: int):
        pass
    
    def get_diff(self, transform_id: int)->pd.DataFrame:
        pass