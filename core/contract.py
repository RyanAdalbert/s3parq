import boto3
import os
from core.helpers.s3_naming_helper import S3NamingHelper as s3Name

from core.constants import ENVIRONMENT, DEV_BUCKET, PROD_BUCKET, UAT_BUCKET, BRANCH_NAME
from core.logging import LoggerMixin

from typing import List


class Contract(LoggerMixin):
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
    DEV = DEV_BUCKET
    PROD = PROD_BUCKET
    UAT = UAT_BUCKET
    STATES = ['raw', 'ingest', 'master', 'enhance',
              'enrich', 'metrics', 'dimensional']

    def __init__(self, parent: str, child: str, state: str, dataset: str, partitions: List[str] = [], partition_size: int = 100, branch=None):
        ''' Set the initial vals to None.
            Default file name, dataset and partitions to empty (they are not required in a contract). 
            Does not support customer / brand aliases
        '''
        attributes = ('branch', 'parent', 'child', 'state',
                      'dataset', 'partitions', 'partition_size')

        self.parent = parent
        self.child = child
        self.state = state
        self.partitions = partitions
        self.dataset = dataset
        self.partition_size = partition_size

        self._set_env()

        if branch is None:
            self._branch = branch
            self._init_branch()
        else:
            self.branch = branch

    @property
    def branch(self)->str:
        return self._branch

    @branch.setter
    def branch(self, branch: str)->None:
        self._branch = self._validate_part(branch)

    @property
    def parent(self)->str:
        return self._parent

    @parent.setter
    def parent(self, parent:str)->None:
        self._parent = self._validate_part(parent)

    @property
    def state(self)->str:
        return self._state

    @state.setter
    def state(self, state: str)->None:
        if state in self.STATES:
            self._state = state
        else:
            raise ValueError(f'{state} is not a valid state')

    @property
    def child(self)->str:
        return self._child

    @child.setter
    def child(self, child: str)->None:
        self._child = self._validate_part(child)

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

    @property
    def previous_state(self)->str:
        ''' INTENT: returns the state before this contract state
            RETURNS: str state name
        '''
        cur = self.STATES.index(self._state)
        if cur < 1:
            return None
        else:
            return self.STATES[cur - 1]

    @property
    def next_state(self)->str:
        ''' INTENT: returns the state after this contract state
            RETURNS: str state name
        '''
        cur = self.STATES.index(self._state)
        if cur == len(self.STATES) - 1:
            return None
        else:
            return self.STATES[cur + 1]

    # Properties that shouldn't be touched from the outside

    @property
    def env(self)->str:
        return self._env

    def _set_env(self)->None:
        env = ENVIRONMENT.lower()
        print (env)
        if env in (self.DEV, 'dev', 'development'):
            self._env = self.DEV
        elif env in (self.PROD, 'prod', 'production'):
            self._env = self.PROD
        elif env in (self.UAT, 'uat'):
            self._env = self.UAT
        else:
            raise ValueError(f'{env} is not a valid environment.')

    def _init_branch(self)->None:
        # set branch default to the git branch.
        # if we need to override this, set the branch param first.
        if self._branch is None:
            try:
                self.branch = BRANCH_NAME
            except:
                raise ValueError(f'Your git branch name {branch_name} cannot be used as a contract branch path.')

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

            # no partitions without a data set
            for p in self.partitions:
                path += f'{p}/'

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

    @property
    def brand(self)->str:
        return self._child

    @brand.setter
    def brand(self, brand: str)->None:
        self.child = brand

    @property
    def customer(self)->str:
        return self._parent

    @customer.setter
    def customer(self, customer: str)->None:
        self.parent = customer

    @property
    def bucket(self)->str:
        return self.env

    @property
    def key(self)->str:
        ''' Removes the s3 domain and the environment prefix'''
        return '/'.join(self.s3_path[5:].split('/')[1:])


    def set_metadata(self, df, run_timestamp):
        df['__metadata_app_version'] = CORE_VERSION
        df['__metadata_run_timestamp'] = run_timestamp
        df['__metadata_output_contract'] = self.get_s3_url()
        partitions = ['__metadata_run_timestamp']
        return (df, partitions)

    def write_with_metadata(self, dataset, df, run_timestamp):
        pass

    # private

    def _validate_part(self, part: str)->str:
        val = s3Name().validate_part(part.lower(), allow_prefix=False)
        if val[0]:
            return part.lower()
        else:
            raise ValueError(val[1])
