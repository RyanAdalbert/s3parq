from typing import List
from datetime import datetime
from pytz import timezone
import pandas as pd
import boto3
import os
import json
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from s3parq import fetch, publish
from core import constants
from core.contract import Contract
from core.helpers.session_helper import SessionHelper as SHelp
from core.models.configuration import RunEvent
import urllib
import urllib.request


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

        path = f's3://{self.env}/{self.branch}/{self.parent}/{self.child}/{self.state}'

        if len(self.dataset) > 0:
            path += f'/{self.dataset}'

        return path
    
    @property
    def redshift_configuration(self)->dict:
        '''Returns the redshift_params for s3parq Redshift Spectrum. All of the configurations come from core_project.yaml
        except for table_name which is set in the format PHARMACOMPANY_BRAND_DATASET_RUNID'''
        redshift_params = dict()
        if constants.ENVIRONMENT == "dev":
            redshift_params['iam_role'] = constants.DEV_REDSHIFT_IAM_ROLE
            redshift_params['cluster_id'] = constants.DEV_REDSHIFT_CLUSTER_ID
            redshift_params['host'] = constants.DEV_REDSHIFT_DB_HOST
        else:
            redshift_params['iam_role'] = constants.REDSHIFT_IAM_ROLE
            redshift_params['cluster_id'] = constants.REDSHIFT_CLUSTER_ID
            redshift_params['host'] = constants.REDSHIFT_DB_HOST
            
        redshift_params['schema_name'] = constants.REDSHIFT_SCHEMA
        redshift_params['db_name'] = constants.REDSHIFT_DB
        redshift_params['port'] = constants.REDSHIFT_DB_PORT
        redshift_params['region'] = constants.REDSHIFT_REGION
        redshift_params['table_name'] = f'{self.parent}_{self.child}_{self.dataset}'

        return redshift_params

    def _set_dev_account(self):
        '''
        To prevent permission issues with Redshift Spectrum, we use a single Core AWS account which is configured via environment variables
        stored in the DEV_AWS_SECRET
        '''
        self.logger.info("Setting environment variables to Core sandbox service account...")
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=constants.AWS_REGION)
        response = client.get_secret_value(SecretId=constants.DEV_AWS_SECRET)['SecretString']
        response = json.loads(response) # The SecretString returned by AWS is a JSON-formatted string parsed as a dict here
        os.environ['AWS_ACCESS_KEY_ID'] = response['AWS_ACCESS_KEY_ID']
        os.environ['AWS_SECRET_ACCESS_KEY'] = response['AWS_SECRET_ACCESS_KEY']   
        return

    # def _set_uat_account(self):
    #     self.logger.info("Setting environment variables to Core dev service account...")
    #     session = boto3.session.Session()
    #     credentials = session.get_credentials()
    #     current_credentials = credentials.get_frozen_credentials()
    #     os.environ['AWS_ACCESS_KEY_ID'] = current_credentials.access_key
    #     os.environ['AWS_SECRET_ACCESS_KEY'] = current_credentials.secret_key
    #     return

    def _format_datetime(self, date: datetime)->str:
        return date.strftime('%Y-%m-%d %H:%M:%S')

    def _set_contract_type(self)->None:
        ''' INTENT: sets what type of contract this is - raw or dataset
            RETURNS: None
        '''
        self._contract_type = "dataset"

    def _set_dataset_metadata(self, df: pd.DataFrame, run_id: int, session: Session):
        try:
            run = session.query(RunEvent).filter(RunEvent.id==run_id).one()
        except NoResultFound:
            raise KeyError("No RunEvent found with id=" + str(run_id) + ".")

        timestamp = run.created_at
        timestamp = timestamp.replace(tzinfo=timezone('UTC'))

        df['__metadata_run_id'] = run_id
        df['__metadata_run_timestamp'] = self._format_datetime(timestamp)
        df['__metadata_app_version'] = constants.CORE_VERSION
        df['__metadata_transform_timestamp'] = self._format_datetime(datetime.utcnow())
        df['__metadata_output_contract'] = self.s3_path

        partitions = ['__metadata_run_id']
        return (df, partitions)

    def _get_server(self):
        ''' Determine if the session is running on an ec2 server.'''
        try:
            self.instance_id = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id',timeout=2).read().decode()
            return "ec2"
        except urllib.error.URLError:
            return "other"

    # functions for use

    def fetch(self, filters: List[dict] = [])->pd.DataFrame:
        if self.contract_type != "dataset":
            raise ValueError(
                f"contract.fetch() method can only be called on contracts of type dataset. This contract is type {self.contract_type}.")
        
        self.logger.info(
            f'Fetching dataframe from s3 location {self.s3_path}.')
        
        return fetch(   bucket = self.env,
                        key = self.key,
                        filters = filters )

    def publish(self, dataframe: pd.DataFrame, run_id: int, session: Session, publish_to_redshift=True)->None:
        if self.contract_type != "dataset":
            raise ValueError(
                f"contract.publish() method can only be called on contracts of type dataset. This contract is type {self.contract_type}.")

        self.logger.info(
            f'Publishing dataframe to s3 location {self.s3_path} with run ID {run_id}.')

        if self._get_server() != "ec2":
            if constants.ENVIRONMENT == 'dev':
                self._set_dev_account()

        dataframe, run_partition = self._set_dataset_metadata(df=dataframe, run_id=run_id, session=session)
        if run_partition not in self.partitions:
            self.partitions.extend(run_partition)

        if publish_to_redshift:
            redshift_params = self.redshift_configuration
            self.logger.debug(f"Publishing dataframe to Redshift Spectrum database {redshift_params['db_name']} to schema.table \
                {redshift_params['schema_name']}.{redshift_params['table_name']}...")
        else:
            redshift_params = None

        publish(
            bucket=self.env,
            key=self.key,
            dataframe=dataframe,
            partitions=self.partitions,
            redshift_params=redshift_params
        )
