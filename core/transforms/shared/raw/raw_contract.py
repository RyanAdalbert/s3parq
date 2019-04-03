import boto3
import os
from core.helpers.s3_naming_helper import S3NamingHelper as s3Name

from core.constants import ENVIRONMENT, DEV_BUCKET, PROD_BUCKET, UAT_BUCKET, BRANCH_NAME
from core.logging import LoggerMixin
from core.helpers.project_root import ProjectRoot

from typing import List
from contextlib import contextmanager

def download_s3_object(bucket: str, key: str, local_dir: str) -> str:
    """
    Download an object from s3 to a specified local directory.
    :param bucket: s3 bucket as a string
    :param key: s3 path to object to download
    :param local_dir: directory to store file
    :return: path of downloaded file
    """
    try:
        s3 = boto3.resource('s3')
        filename = os.path.split(key)[-1]
        local_path = os.path.join(local_dir, filename)
        s3.Bucket(bucket).download_file(key, local_path)

        return local_path
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            raise FileNotFoundError(f"s3 object not found: s3://{bucket}/{key}")
        else:
            raise

class RawContract(LoggerMixin):
    ''' *** This is specific to the raw state! ***
        The s3 contract is how we structure our data lake. 
        This contract defines the output structure of data into S3.
        *--------------------------------------------------------------------*
        | contract structure in s3:                                          |
        |                                                                    |
        | s3:// {ENV} / {BRANCH} / {PARENT} / {CHILD} / {STATE} / {FILENAME} |
        |                                                                    |
        *--------------------------------------------------------------------*
        ENV - environment Must be one of development, uat, production. 
            Prefixed with integrichain- due to global unique reqirement
        BRANCH - the software branch for development this will be the working pull request (eg pr-225)
            in uat this will be edge, in production this will be master
        PARENT - The top level source identifier 
            this is generally the customer (and it is aliased as such) but can be IntegriChain for internal sources,
            or another aggregator for future-proofing
        CHILD - The sub level source identifier, generally the brand (and is aliased as such) 
        STATE - One of: raw or ingest
    '''
    DEV = DEV_BUCKET
    PROD = PROD_BUCKET
    UAT = UAT_BUCKET
    STATES = ['raw', 'ingest']

    def __init__(self, parent: str, child: str, state: str, branch: str = None):
        ''' Initialize with the key params
            Branch can pull from environment variables though so not required
        '''

        self.parent = parent
        self.child = child
        self.state = state
        
        self._set_env()

        if branch is None:
            self._branch = branch
            self._set_branch()
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

    def _set_branch(self)->None:
        # set branch default to the git branch.
        # if we need to override this, set the branch param first.
        if self.branch is None:
            try:
                self.branch = BRANCH_NAME
            except:
                raise ValueError(f'Your git branch name {branch_name} cannot be used as a contract branch path.')

    def raw_get_s3_path(self, filename='')->str:
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
                'raw_get_s3_path() requires all contract params to be set.')

        path = f's3://{self.env}/{self.branch}/{self.parent}/{self.child}/{self.state}/'

        path += filename
        return path

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

    # Outside functions

    def publish_raw_file(self, local_file_path: str) ->None:
        '''accepts a local path to a file, publishes it as-is to s3 as long as state == raw.'''
        if self.state != 'raw':
            raise ValueError(
                'publish_raw_file may only be used on raw contracts.')

        s3_client = boto3.client('s3')
        filename = os.path.split(local_file_path)[1]
        key = self.key+filename
        self.logger.info(f'Publishing a local file at {local_file_path} to s3 location {self.raw_get_s3_path(filename)}.')

        with open(local_file_path, 'rb') as file_data:
            extra_args = {'source_modified_time': str(
                float(os.stat(local_file_path).st_mtime))}
            resp = s3_client.upload_fileobj(file_data, Bucket=self.bucket, 
                Key=key, ExtraArgs={"Metadata": extra_args})

    def get_raw_file_metadata(self, local_file_path:str) ->None:
        # If file exists, return its metadata
        s3_client = boto3.client('s3')
        
        filename = os.path.split(local_file_path)[1]
        key = self.raw_get_s3_path(filename)
        try:
            return s3_client.head_object(Bucket=self.bucket,Key=key)["Metadata"]
        except ClientError as e:
            # If file does not exist, throw back since it needs to be moved anyways
            #   Consider: cleaner handling?
            if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
                raise KeyError("File not found!")
            else:
                raise e

    def list_files(self, file_prefix='') -> List[str]:
        key = self.key
        keyfix = key+file_prefix
        try:
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(self.bucket)
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
            download_path = download_s3_object(self.bucket, self.key+filename, tmp_dir)
            yield download_path

    # aliases

    @property
    def bucket(self)->str:
        return self.env

    @property
    def key(self)->str:
        ''' Removes the s3 domain and the environment prefix'''
        return '/'.join(self.raw_get_s3_path()[5:].split('/')[1:])

    @property
    def brand(self)->str:
        return self._child

    @brand.setter
    def brand(self, brand: str)->None:
        self.child = brand

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
