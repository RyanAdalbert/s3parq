from core.helpers import configuration_mocker, file_mover
from core.models import configuration
from core import secret, contract

import os
import tempfile

def test_run_extract_transform(env:str,transform_id:int,branch:str,manufacturer:str,brand:str):
    # TODO: This is currently using the config mocker to generate configs to run against
    #   When configs are ready, switch out to appropriate functions

    # Mocking configs for use in extract testing
    config_mock = configuration_mocker.ConfigurationMocker()
    config_mock.generate_mocks()

    session = config_mock.get_session()

    ec = configuration.ExtractConfiguration
    t = configuration.Transformation

    # Start querying the extract configs
    q = session.query(t).filter(t.id == transform_id)
    for f_transform in q:
        transform_state = str.lower(f_transform.pipeline_state.pipeline_state_type.name)
        for extract in f_transform.extract_configurations:
            output_contract = contract.Contract(env=env,
                                                state=transform_state,
                                                branch=branch,
                                                parent=manufacturer,
                                                child=brand
                                                )
            extract_transform = ExtractTransform(env=env, mock_config=extract,output_contract=output_contract)
            extract_transform.test_run()


class ExtractTransform():
    def __init__(self, env:str, mock_config, output_contract):
        self.env = env
        self.config=mock_config
        self.output_contract = output_contract

    def test_run(self):
        # Set values from extract config
        remote_path = self.config.filesystem_path
        prefix = self.config.prefix
        secret_name = self.config.secret_name

        # Fetch secret from secret contract
        # TODO: Currently configs made for FTP only, FTP type passed in directly
        source_secret = secret.Secret(name=self.config.secret_name,env=self.env,type_of="FTP",mode="write")
        
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
