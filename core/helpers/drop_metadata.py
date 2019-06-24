import pandas as pd

meta_cols = dict(__metadata_run_id="integer",
               __metadata_run_timestamp="datetime",
               __metadata_output_contract="string",
               __metadata_app_version="float",
               __metadata_transform_timestamp="datetime")

def get_meta_cols():
    return meta_cols

def drop_metadata(df: pd.DataFrame):
    return df.drop(columns=list(meta_cols.keys()))
