"""
This is a simple aggregation of the main functionality used in the 
    ingest column mapping transforms.
This is split off due to the duplication across the expected 5+ transforms.
"""

import boto3
import pandas as pd
from typing import Dict, List

from core.logging import LoggerSingleton


logger = LoggerSingleton().logger


# Custom exception class, this makes exception handling specific
# Given the try except, other exceptions could catch valid errors occuring
class MissingRequiredColumnError(Exception):
    """ This class is meant to be an Exception thrown only when dataframes are 
        received without all the specific required columns.
        Possibly later may get a notification option.
    """
    pass


def check_required_columns(df: pd.DataFrame, column_renames: Dict, required_columns: List)->None:
    """ This function take a dataframe and ensures it has the required columns.
        It uses the column renames dictionary to check from the specified 
        required columns official schema to compare to the pre-mapped columns.
        This does not return anything but rather throws a (custom)
        MissingRequiredColumnError exception on failure.

    Args:
        df (pd.DataFrame): The dataframe to check
        column_renames (Dict): The mappings of columns (key=end,value=pre-map)
        required_columns (List): A list of string column names to ensure exist

    Returns:
        None

    """

    logger.debug(f"Expecting the following columns : {list(column_renames.values())}")
    logger.debug(f"Dataframe has these columns : {list(df.columns)}")

    # Gets the pre-mapping required column names
    required_columns_preschema = [value for key,value in column_renames.items() if key in required_columns]
    
    logger.debug(f"The following columns are required : {required_columns_preschema}")
    
    missing_required_columns = set(required_columns_preschema) - set(df.columns)

    if missing_required_columns:
        logger.error("Data does not have all required columns.")
        raise MissingRequiredColumnError(f"Missing required columns : {missing_required_columns}")


def rename_and_correct_shape(df: pd.DataFrame, column_renames: Dict)->pd.DataFrame:
    """ This function take a dataframe and modifies it to match the definition
        of the column renames dict.
        This will:
            - Drop columns not in the rename dictionary
            - Rename matching columns from the source to the specified
            - Create columns that are in the dictionery but not the dataframe
                and fill them with empty strings

    Args:
        df (pd.DataFrame): The dataframe to modify
        column_renames (Dict): The mappings of columns (key=end,value=pre-map)

    Returns:
        The modified dataframe

    """
    # First cut down to the necesarry columns in case of accidental extras - Pandas wont catch those
    extra_columns = set(df.columns) - set(column_renames.values())
    df = df.drop(axis=1,labels=list(extra_columns))

    # Reverse dictionary made since theres a clash in order needs
    # More complicated case to handle duplicate column mappings
    column_renames_pandas_style = {}
    duplicate_columns = {}

    for key, value in column_renames.items():
        if value == "":
            continue

        if value not in column_renames_pandas_style:
            column_renames_pandas_style[value] = key
        else:
            if value not in duplicate_columns:
                duplicate_columns[value] = [key]
            else:
                duplicate_columns[value].append(key)

    for key, value in duplicate_columns.items():
        for v in value:
            df[v] = df[key]

    df = df.rename(column_renames_pandas_style, axis="columns")
    # All the stuff above makes the order unpredictable client-to-client
    df = df.reindex(list(column_renames.keys()),axis='columns')

    # Add missing columns to match schema and fill with empty strings
    missing_columns = set(column_renames.keys()) - set(df.columns)
    for column in missing_columns:
        df[column] = ""

    return df


def retrieve_initial_ingest_file_names(bucket: str, file_path_prefix: str)->List:
    """ This function take the dataset spit out by Initial Ingest and
        returns the names from the actual files based on the pathing.
        It does this by reading all files, removing the file path prefix from
        their names, removing partitions and parquet parts, and returning all
        unique values left.
    
    (This is based on Initial Ingest at version as of 8/23/2019)

    Args:
        bucket (str): The bucket of the file list
        file_path_prefix (str): The prefix to the file list

    Returns:
        The list of file names from the Initial Ingest format

    """
    # Get names of all files under key
    file_names = set()
    files_with_prefix = []
    s3_client = boto3.client('s3')
    paginator = s3_client.get_paginator('list_objects')
    operation_parameters = {'Bucket': bucket,
                            'Prefix': file_path_prefix}
    page_iterator = paginator.paginate(**operation_parameters)
    for page in page_iterator:
        if not "Contents" in page.keys():
            break

        for item in page['Contents']:
            if item['Key'].endswith('.parquet'):
                files_with_prefix.append(item['Key'])
                
    key_len = len(file_path_prefix)

    def subtract_key(file):
        # +1 due to the extra slash at the end
        return file[(key_len + 1):]

    files_without_prefix = [subtract_key(file) for file in files_with_prefix]

    for file_path in files_without_prefix:
        # Split up so other parts can be easily deleted
        unparsed_parts = file_path.split("/")
        
        # Remove parquet names at the end
        del unparsed_parts[-1]

        # Remove all partition columns
        for part in unparsed_parts:
            if "=" not in part:
                file_names.add(part)
    
    return file_names
