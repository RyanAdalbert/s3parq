import logging
from git import Repo
from helpers.s3_naming_helper import S3NamingHelper as s3Name

class Contract:
    ''' The s3 contract is how we structure our data lake. 
        This contract defines the output structure of data into S3.
        *--------------------------------------------------------------------------------------------------------------------*
        | contract structure in s3:                                                                                          |
        |                                                                                                                    |
        | s3:// {ENV} / {BRANCH} / {PARENT} / {CHILD} / {STATE} / {DATASET} / {PARTITION} [ / {SUB-PARTITION} / ] {FILENAME} |
        |                                                                                                                    |
        *--------------------------------------------------------------------------------------------------------------------*
        ENV - environment Must be one of development, uat, production. 
            Prefixed with integrichain- due to global unique reqirement
        BRANCH - the software branch for development this will be the working pull request (eg pr-225)
            in uat this will be edge, in production this will be master
        PARENT - The top level source identifier 
            this is generally the customer (and it is aliased as such) but can be IntegriChain for internal sources,
            or another aggregator for future-proofing
        CHILD - The sub level source identifier, generally the brand (and is aliased as such) 
        STATE - One of: Raw, Ingest, Master, Enhance, Enrich, Metrics 
        DATASET - The name of the collection of data. In an RDBMS this would be a table or view
        PARTITION - for datasets, the partition is set in the prefix name  
        SUB-PARTITION - for datasets, the sub-partitions add additional partitioning with additional prefixes
        FILENAME - nondescript in the contract
    '''    
    DEV = 'ichain-development'
    PROD = 'ichain-production'
    UAT = 'ichain-uat'
    STATES = ['Raw','Ingest','Master','Enhance','Enrich','Metrics','Dimensional']

    def __init__(self, **kwargs):
        ''' Set the initial vals to None.
            Default file name, dataset and partitions to empty (they are not required in a contract). 
            Does not support customer / brand aliases
        '''
        attributes = ('branch','env','parent','child','state','dataset', 'file_name', 'partitions', 'partition_size')    

        for attr in attributes:
            self.__dict__[attr] = None

        ## defaults
        self.file_name = str()
        self.partitions = []
        self.dataset = str()
        self.partition_size = 100 ## partition size in mb
        self.contract_type = 'state'

        ## set the attributes using the setter methods if they are in kwargs
        for attr in attributes:
            if attr in kwargs:
                setter = getattr(self,'set_' + attr)
                setter(kwargs[attr])




    def get_branch(self):
        return self.branch
       
    def get_parent(self):
        return self.parent

    def get_state(self):
        return self.state

    def get_child(self):
        return self.child

    def get_env(self):
        return self.env

    def get_dataset(self):
        return self.dataset
    
    def get_partitions(self):
        return self.partitions

    def get_partition_size(self):
        return self.partition_size
    
    def get_file_name(self):
        return self.file_name
    
    def get_contract_type(self):
        return self.contract_type

    def get_previous_state(self):
        ''' INTENT: returns the state before this contract state
            RETURNS: str state name
        '''
        cur = self.STATES.index(self.state)
        if cur > 1:
            return None
        else:
            return self.STATES[cur - 1]

    def get_next_state(self):
        ''' INTENT: returns the state after this contract state
            RETURNS: str state name
        '''
        cur = self.STATES.index(self.state)
        if cur == len(self.STATES) - 1:
            return None
        else:
            return self.STATES[cur + 1]

    def set_branch(self, branch):
        self.branch = self._part_formatter(branch)

    def set_parent(self, parent):
        self.parent = self._part_formatter(parent)
    
    def set_child(self, child):
        self.child = self._part_formatter(child)

    def set_state(self,state):
        if state.capitalize() in self.STATES:
            self.state = state.capitalize()

    def set_dataset(self,dataset):
        ## leave in natural case for datasets
        self.dataset = self._validate_part(dataset)             
        self._set_contract_type()

    def set_partition_size(self,size):
        self.partition_size = size
    
    def set_partitions(self,partitions):
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
        self.partitions = temp_partitions
        self._set_contract_type()

    def set_file_name(self,file_name):
        self.file_name = self._validate_part(file_name)
        self._set_contract_type()

    def set_env(self, env):
        env = env.lower()
        if env in (self.DEV, 'dev','development'):
            self.env = self.DEV
        elif env in (self.PROD, 'prod','production'):
            self.env = self.PROD
        elif env in (self.UAT, 'uat'):
            self.env = self.UAT
        else:
            raise ValueError(f'{env} is not a valid environment.')

        ## set branch default to the git branch.
        ## if we need to override this, set the branch param first.
        if self.branch is None:
            try:
                self.set_branch(Repo('.').active_branch.name) 
            except:
                raise ValueError('Your git branch name cannot be used as a contract branch path.')

    def _set_contract_type(self):
        ''' INTENT: sets what type of contract this is - file, partition, or dataset
            RETURNS: None
        '''
        if len(self.file_name) > 0:
            t = 'file'
        elif len(self.partitions) > 0:
            t = 'partition'
        elif len(self.dataset) > 0:
            t = 'dataset'
        else:
            t = 'state'
        self.contract_type = t

    def get_s3_path(self):
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
            raise ValueError('get_s3_path() requires all contract params to be set.')
        
        path = f's3://{self.env}/{self.branch}/{self.parent}/{self.child}/{self.state}/'

        if len(self.dataset) > 0:
            path += f'{self.dataset}/'
          
            ## no partitions without a data set
            for p in self.partitions:
                path += f'{p}/'
        
        path += self.file_name
        return path   

    ##TODO: move publish() in here (should write accept a pandas df and optional schema and write parquet to contract).
    
    def set_parquet_schema(self, schema):
        ''' INTENT: sets the schema, a pyarrow parquet schema object.
            RETURNS: None
        '''
        self.parquet_schema = schema


    ## aliases
    def get_brand(self):
        return self.get_child()

    def get_customer(self):
        return self.get_parent()

    def set_brand(self,val):
        self.set_child(val)

    def set_customer(self):
        self.set_brand(val)

    def get_bucket(self):
        return self.get_env()
    
    def get_key(self):
        ''' Removes the s3 domain and the environment prefix'''
        return '/'.join(self.get_s3_path()[5:].split('/')[1:])

    def set_bucket(self,env):
        self.set_env(env)

    ## private
    def _part_formatter(self,part):
        part = part.capitalize()
        return self._validate_part(part)
    
    def _validate_part(self,part):
        val = s3Name().validate_part(part, allow_prefix = False)
        if val[0]:
            return part
        else:
            raise ValueError(val[1])

