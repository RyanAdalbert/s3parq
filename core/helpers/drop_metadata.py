import pandas as pd


def drop_metadata(df: pd.DataFrame):
    meta_cols = ["__metadata_app_version", "__metadata_output_contract", "__metadata_run_timestamp", "__metadata_run_id", "__metadata_transform_timestamp"]
    return df.drop(columns=meta_cols)
