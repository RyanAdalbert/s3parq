import boto3
import os
import pandas as pd
from s3parq.s3_naming_helper import S3NamingHelper as s3Name
from s3parq import publish,fetch    
from core.constants import ENVIRONMENT, DEV_BUCKET, PROD_BUCKET, UAT_BUCKET, BRANCH_NAME
from core.logging import LoggerMixin

from typing import List


class Contract(LoggerMixin):
    ''' This class is the base contracts for all other typed contracts.
        The s3 contract is how we structure our data lake. 
        This contract defines the output structure of data into S3.
        *-------------------------------------------------------*
        | contract structure in s3:                             |
        |                                                       |
        | s3:// {ENV} / {BRANCH} / {PARENT} / {CHILD} / {STATE} |
        |                                                       |
        *-------------------------------------------------------*
        ENV - environment Must be one of development, uat, production. 
            Prefixed with integrichain- due to global unique reqirement
        BRANCH - the software branch for development this will be the working pull request (eg pr-225)
            in uat this will be edge, in production this will be master
        PARENT - The top level source identifier 
            this is generally the customer (and it is aliased as such) but can be IntegriChain for internal sources,
            or another aggregator for future-proofing
        CHILD - The sub level source identifier, generally the brand (and is aliased as such) 
        STATE - One of: raw, ingest, master, enhance, Enrich, Metrics 
    '''
    DEV = DEV_BUCKET
    PROD = PROD_BUCKET
    UAT = UAT_BUCKET
    STATES = ['raw', 'ingest', 'master', 'enhance',
              'enrich', 'metrics', 'dimensional']

    def __init__(self, parent: str, child: str, state: str, branch=None):
        ''' Set the initial vals to None.
            Default file name, dataset and partitions to empty (they are not required in a contract). 
            Does not support customer / brand aliases
        '''
        attributes = ('branch', 'parent', 'child', 'state',
                      'dataset', 'partitions', 'partition_size')

        self.parent = parent
        self.child = child
        self.state = state
        self._contract_type = "state"

        self._set_env()

        if branch is None:
            self._branch = branch
            self._init_branch()
        else:
            self.branch = branch

    @property
    def branch(self)->str:
        return self._branch

<<<<<<< HEAD
    @branch.setter
    def branch(self, branch: str)->None:
        self._branch = self._validate_part(branch)
=======
    @property
    def env(self)->str:
        return self._env

    def get_branch(self)->str:
        return self.branch
>>>>>>> 1737ec98bbf6c97c6d46ba295499e721315f2467

    @property
    def parent(self)->str:
        return self._parent

    @parent.setter
    def parent(self, parent:str)->None:
        self._parent = self._validate_part(parent)

    @property
    def state(self)->str:
        return self._state

<<<<<<< HEAD
    @state.setter
    def state(self, state: str)->None:
        if state in self.STATES:
            self._state = state
        else:
            raise ValueError(f'{state} is not a valid state')
=======
    def get_env(self)->str:
        self.logger.warning("get_env is depricated. Use env instead.")
        return self._env

    def get_dataset(self)->str:
        return self.dataset
>>>>>>> 1737ec98bbf6c97c6d46ba295499e721315f2467

    @property
    def child(self)->str:
        return self._child

    @child.setter
    def child(self, child: str)->None:
        self._child = self._validate_part(child)

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
                raise ValueError(
                    f'Your git branch name {branch_name} cannot be used as a contract branch path.')

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

        return path

<<<<<<< HEAD
=======
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
            f'Publishing dataframe to s3 location {self.get_s3_path()}.')

        publish(
            bucket=self.env,
            key=self.get_key(),
            dataframe=dataframe,
            partitions=partitions
        )

    def publish_raw_file(self, local_file_path: str) ->None:
        '''accepts a local path to a file, publishes it as-is to s3 as long as state == raw.'''
        if self.get_state() != 'raw':
            raise ValueError(
                'publish_raw_file may only be used on raw contracts.')

        s3_client = boto3.client('s3')

        filename = os.path.split(local_file_path)[1]
        key = self.get_key()+filename
        self.logger.info(f'Publishing a local file at {local_file_path} to s3 location {self.get_s3_path()+filename}.')

        with open(local_file_path, 'rb') as file_data:
            extra_args = {'source_modified_time': str(
                float(os.stat(local_file_path).st_mtime))}
            resp = s3_client.upload_fileobj(file_data, Bucket=self.get_bucket(
            ), Key=key, ExtraArgs={"Metadata": extra_args})

    def get_raw_file_metadata(self, local_file_path: str) ->None:
        # If file exists, return its metadata
        s3_client = boto3.client('s3')

        filename = os.path.split(local_file_path)[1]
        key = self.get_key()+filename
        return s3_client.head_object(Bucket=self.get_bucket(),Key=key)


    def list_files(self, file_prefix='') -> List[str]:
        key = self.get_key()
        keyfix = key+file_prefix
        try:
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(self.get_bucket())
            objects = [obj.key for obj in bucket.objects.filter(Prefix=keyfix)]

            return objects
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                raise FileNotFoundError("s3 object not found: %s" % file_prefix)
            else:
                raise

    @contextmanager
    def download_raw_file(self, filename):
        with tempfile.TemporaryDirectory() as tmp_dir:
            download_path = download_s3_object(self.get_bucket(), self.get_key()+filename, tmp_dir)
            yield download_path


>>>>>>> 1737ec98bbf6c97c6d46ba295499e721315f2467
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

    # private

    def _validate_part(self, part: str)->str:
        val = s3Name().validate_part(part.lower(), allow_prefix=False)
        if val[0]:
            return part.lower()
        else:
            raise ValueError(val[1])
