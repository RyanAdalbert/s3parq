from core.helpers import file_mover
from core.models import configuration
from core import secret, contract
from core.constants import ENVIRONMENT

import os
import tempfile

class ExtractTransform():
    
    def __init__(self, **kwargs) -> None:
        """ Performs the extraction to a given output contract. 
            Valid kwargs:
                - transform a configuration contract instance
                - output_contract a contract instance
        """
        self.REQUIRED_PARAMS = ('output_contract','transform')
        
        for attr in self.REQUIRED_PARAMS:
            self.__dict__[attr] = None

        self.set_env()

        for attr in self.REQUIRED_PARAMS:
            if attr in kwargs:
                setter = getattr(self, 'set_' + attr)
                setter(kwargs[attr])


    def set_env(self)->None:
        env = ENVIRONMENT
        if env in ('dev','prod','uat'):
            self.env = env
        else:
            raise ValueError(f'{env} is not a valid environment')
    
    def set_transform(self, transform: configuration.Transformation) -> None:
        self.transform = transform
    
    def set_output_contract(self, output_contract: contract) -> None:
        self.output_contract = output_contract


    def run(self):
        for config in self.transform.extract_configurations:
            # Set values from extract config
            remote_path = config.filesystem_path
            prefix = config.prefix
            secret_name = config.secret_name
            secret_type_of = config.secret_type_of

            # Fetch secret from secret contract
            # TODO: Currently configs made for FTP only, FTP type passed in directly
            source_secret = secret.Secret(name=secret_name,type_of=secret_type_of,mode="write")
            
            # Get files from remote and start pushing to s3
            with tempfile.TemporaryDirectory() as tmp_dir:
                file_mover.get_files(tmp_dir=tmp_dir,prefix=prefix,remote_path=remote_path,secret=source_secret)
                self.push_to_s3(tmp_dir, self.output_contract)
                
    def push_to_s3(self, tmp_dir: str, output_contract: contract)-> None:
        """ For a local file dir, push the file to s3 if it is newer or does not exist."""
        self._validate_required_params()

        # For each local file, see (by the set metadata) if it needs to be pushed to S3 by the constraints
        for local_file in os.listdir(f"{tmp_dir}"):
            local_file_path = os.path.join(tmp_dir,local_file)
            local_file_modified_time = os.stat(os.path.join(tmp_dir,local_file)).st_mtime

            if (self._file_needs_update(output_contract=output_contract,
                                        local_file_path=local_file_path,
                                        local_file_modified_time=local_file_modified_time
                                        )):
                output_contract.publish_raw_file(local_file_path)

    def _file_needs_update(self,output_contract: contract,local_file_path: str,local_file_modified_time: str)-> None:
        """ Check if file needs to be pushed
            File is only considered to need to be pushed if it does not exist or has been modified since last push
        """
        try:
            s3_last_modified = output_contract.get_raw_file_metadata(local_file_path)['Metadata']['source_modified_time']
            if (float(s3_last_modified) < float(local_file_modified_time)):
                return True
            else:
                return False
        except:
            return True

    def _validate_required_params(self) -> bool: 
        ''' Checks that all required params are set '''
        for param in self.REQUIRED_PARAMS:
            if param not in self.__dict__.keys():
                raise ValueError(f'{param} is a required value not set for ExtractTransform.')
