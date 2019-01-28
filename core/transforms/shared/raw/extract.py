from core.helpers import file_mover
from core.models import configuration
from core import secret, contract

import os
import tempfile

class ExtractTransform():
    def __init__(self, env:str, transform, output_contract):
        self.env = env
        self.output_contract = output_contract
        self.transform = transform

    def run(self):
        for config in self.transform.extract_configurations:
            # Set values from extract config
            remote_path = config.filesystem_path
            prefix = config.prefix
            secret_name = config.secret_name

            # Fetch secret from secret contract
            # TODO: Currently configs made for FTP only, FTP type passed in directly
            source_secret = secret.Secret(name=config.secret_name,env=self.env,type_of="FTP",mode="write")
            
            # Get files from remote and start pushing to s3
            with tempfile.TemporaryDirectory() as tmp_dir:
                file_mover.get_files(tmp_dir=tmp_dir,prefix=prefix,remote_path=remote_path,secret=source_secret)
                self.push_to_s3(tmp_dir)
                
    
    def push_to_s3(self, tmp_dir):
        # Get the transformation's output contract
        oc = self.output_contract

        # For each local file, see (by the set metadata) if it needs to be pushed to S3 by the constraints
        for local_file in os.listdir(f"{tmp_dir}"):
            local_file_path = os.path.join(tmp_dir,local_file)
            local_file_modified_time = os.stat(os.path.join(tmp_dir,local_file)).st_mtime

            if (self._file_needs_update(local_file_path,local_file_modified_time)):
                self.output_contract.publish_raw_file(local_file_path)

    def _file_needs_update(self,local_file_path,local_file_modified_time):
        # Check if file needs to be pushed
        #   File is only considered to need to be pushed if it does not exist or has been modified since last push
        output_contract = self.output_contract

        try:
            s3_last_modified = output_contract.get_raw_file_metadata(local_file_path)['Metadata']['source_modified_time']
            if (float(s3_last_modified) < float(local_file_modified_time)):
                return True
            else:
                return False
        except:
            return True
