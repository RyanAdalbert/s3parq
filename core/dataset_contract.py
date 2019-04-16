import pandas as pd
from s3parq import fetch, publish
from typing import List

from core.contract import Contract

class DatasetContract(Contract):
    ''' The s3 contract is how we structure our data lake. 
        This contract defines the output structure of data into S3.
        *---------------------------------------------------------------------------------------------------------*
        | contract structure in s3:                                                                               |
        |                                                                                                         |
        | s3:// {ENV} / {BRANCH} / {PARENT} / {CHILD} / {STATE} / {DATASET} / {PARTITION} [ / {SUB-PARTITION} / ] |
        |                                                                                                         |
        *---------------------------------------------------------------------------------------------------------*
        ENV - environment Must be one of development, uat, production. 
            Prefixed with integrichain- due to global unique reqirement
        BRANCH - the software branch for development this will be the working pull request (eg pr-225)
            in uat this will be edge, in production this will be master
        PARENT - The top level source identifier 
            this is generally the customer (and it is aliased as such) but can be IntegriChain for internal sources,
            or another aggregator for future-proofing
        CHILD - The sub level source identifier, generally the brand (and is aliased as such) 
        STATE - One of: raw, ingest, master, enhance, Enrich, Metrics 
        DATASET - The name of the collection of data. In an RDBMS this would be a table or view
        PARTITION - for datasets, the partition is set in the prefix name  
        SUB-PARTITION - for datasets, the sub-partitions add additional partitioning with additional prefixes
    '''

    def __init__(self, parent: str, child: str, state: str, dataset: str, partitions: List[str] = [], partition_size: int = 100, branch=None):
        ''' Set the initial vals to None.
            Calls the common attributes to super, though some are 
            Default file name, dataset and partitions to empty (they are not required in a contract). 
        '''

        super().__init__(parent=parent, child=child, state=state, branch=branch)

        self.partitions = partitions
        self.dataset = dataset
        self.partition_size = partition_size


    @property
    def dataset(self)->str:
        return self._dataset

    @dataset.setter
    def dataset(self, dataset: str)->None:
        # leave in natural case for datasets
        self._dataset = dataset
        self._set_contract_type()

    @property
    def partitions(self)->str:
        return self._partitions

    @partitions.setter
    def partitions(self, partitions: list)->None:
        ''' INTENT: sets the partitions for a contract
            ARGS:
                - partitions (list) an ordered list of partition names.
                    will be applied in list order
            RETURNS: None
        '''
        self._partitions = partitions
        self._set_contract_type()

    @property
    def contract_type(self)->str:
        return self._contract_type

    # Properties that shouldn't be touched from the outside

    @property
    def s3_path(self)->str:
        ''' INTENT: builds the s3 path from the contract.
            RETURNS: string s3 path
            NOTE: requires all params to be set to at least the state level
        '''
        if not (self.env and
                self.branch and
                self.parent and
                self.child and
                self.state
                ):
            raise ValueError(
                's3_path requires all contract params to be set.')

        path = f's3://{self.env}/{self.branch}/{self.parent}/{self.child}/{self.state}/'

        if len(self.dataset) > 0:
            path += f'{self.dataset}/'

        return path

    def _set_contract_type(self)->None:
        ''' INTENT: sets what type of contract this is - file, partition, or dataset
            RETURNS: None
        '''
        if len(self.partitions) > 0:
            t = 'partition'
        else:
            t = 'dataset'

        self._contract_type = t

    # functions for use

    def fetch(self, filters: List[dict])->pd.DataFrame:
        if self.contract_type != "dataset":
            raise ValueError(
                f"contract.fetch() method can only be called on contracts of type dataset. This contract is type {self.contract_type}.")
        
        self.logger.info(
            f'Fetching dataframe from s3 location {self.get_s3_path()}.')
        
        return fetch(   bucket = self.env,
                        key = self.get_key(),
                        filters = filters )

    def publish(self, dataframe: pd.DataFrame, partitions: List[str])->None:
        if self.contract_type != "dataset":
            raise ValueError(
                f"contract.publish() method can only be called on contracts of type dataset. This contract is type {self.contract_type}.")

        self.logger.info(
            f'Publishing dataframe to s3 location {self.s3_path}.')

        publish(
            bucket=self.env,
            key=self.key,
            dataframe=dataframe,
            partitions=partitions
        )

    # aliases

    def set_metadata(self, df, run_timestamp):
        # df['__metadata_app_version'] = CORE_VERSION
        df['__metadata_run_timestamp'] = run_timestamp
        df['__metadata_run_timestamp'] = df['__metadata_run_timestamp'].astype(str)
        df['__metadata_output_contract'] = self.s3_path
        partitions = ['__metadata_run_timestamp']
        df = df.astype(str)
        return (df, partitions)

    def write_with_metadata(self, df, run_timestamp):
        df, partitions = self.set_metadata(df=df,run_timestamp=run_timestamp)
        print (partitions)
        print (df.head())
        self.publish(dataframe=df,partitions=partitions)
