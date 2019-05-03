from s3parq.s3_naming_helper import S3NamingHelper as s3Name
from core.contract import Contract

from typing import List

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

    def __init__(self, parent: str, child: str, state: str, dataset: str, partitions: List[str] = [], branch=None):
        ''' Set the initial vals to None.
            Calls the common attributes to super, though some are 
            Default file name, dataset and partitions to empty (they are not required in a contract). 
        '''

        super().__init__(parent=parent, child=child, state=state, branch=branch)

        self.partitions = partitions
        self.dataset = dataset

    @property
    def dataset(self)->str:
        return self._dataset

    @dataset.setter
    def dataset(self, dataset: str)->None:
        # leave in natural case for datasets
        self._dataset = self._validate_part(dataset)
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
        temp_partitions = []
        for p in partitions:
            val = s3Name().validate_part(p)
            if val[0]:
                temp_partitions.append(p)
            else:
                raise ValueError(val[1])
        self._partitions = temp_partitions
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

        path = f's3://{self.env}/{self.branch}/{self.parent}/{self.child}/{self.state}'

        if len(self.dataset) > 0:
            path += f'/{self.dataset}'

            # no partitions without a data set
            for p in self.partitions:
                path += f'/{p}'

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

    # aliases

    def set_metadata(self, df, run_timestamp):
        df['__metadata_app_version'] = CORE_VERSION
        df['__metadata_run_timestamp'] = run_timestamp
        df['__metadata_output_contract'] = self.get_s3_url()
        partitions = ['__metadata_run_timestamp']
        return (df, partitions)

    def write_with_metadata(self, dataset, df, run_timestamp):
        pass
