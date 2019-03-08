from core.models.configuration import (
    PipelineState, 
    PipelineStateType, 
    TransformationTemplate, 
    Transformation,
    InitialIngestTransformation,
    InitialIngestConfiguration
)

from core.helpers.configuration_mocker import setup_base_session
from core.transforms.shared.ingest.ingest import InitialIngestTransform
from core.transforms.shared.ingest import ingest
from mock import patch, PropertyMock, MagicMock
import pytest
import pandas as pd
import tempfile
import boto3
import moto
import time
import core.contract as contract
from core.constants import ENV_BUCKET
import os

def get_filename_from_path(file):
    return os.path.split(file.name)[1]

class Test:
    @moto.mock_s3
    def setup_session(self):
        client = boto3.client('s3')
        client.create_bucket(Bucket= ENV_BUCKET)
        
        raw_file = tempfile.NamedTemporaryFile(prefix='BRIOVA_')
        raw_file.write(b'werds,numbers\nhello,1\nworld,2')
        input_contract = contract.Contract(branch='master', parent='bluth', child='cornballer', state='raw')
        output_contract = contract.Contract(branch='master', parent='bluth', child='cornballer', state='ingest')
        
        key = input_contract.get_key()+get_filename_from_path(raw_file)
        client.upload_file(Bucket=ENV_BUCKET, Filename= raw_file.name, Key=key
        , ExtraArgs={"Metadata": {"source_modified_time": str(time.time())}})

        session = setup_base_session()
        session.add(PipelineStateType(id=1, name='ingest'))
        session.add(PipelineState(id=1, pipeline_state_type_id=1,
                                  graph_order=1, pipeline_id=1))
        session.add(TransformationTemplate(id=1, name='initial_ingest'))
        session.add(InitialIngestTransformation(id=1, graph_order=0, transformation_template_id=1, pipeline_state_id=1))
        session.commit()

        return (session, input_contract, output_contract)

    def test_ingest_validate_config(self):
        session, input_contract, output_contract = self.setup_session()
        good_ii_config = InitialIngestConfiguration(transformation_id=1, delimiter=',', skip_rows=0, encoding="utf8",
            input_file_prefix="BRIOVA_", dataset_name="patient_status")
        session.add(good_ii_config)
        session.commit()

        ingest.validate_config(good_ii_config)

        bad_encoding_ii_config = InitialIngestConfiguration(transformation_id=1, delimiter=',',
            skip_rows=0, encoding="brupbrup", input_file_prefix="BRIOVA_", dataset_name="patient_status")
        with pytest.raises(ValueError):
            ingest.validate_config(bad_encoding_ii_config)

        bad_delimiter_ii_config = InitialIngestConfiguration(transformation_id=1, delimiter='',
            skip_rows=0, encoding="brupbrup", input_file_prefix="BRIOVA_", dataset_name="patient_status")
        with pytest.raises(ValueError):
            ingest.validate_config(bad_delimiter_ii_config)

        assert True

    def test_ingest_set_initial_metadata(self):
        df = pd.DataFrame(['hello','world'], columns=["werds"])
        s3_url = "s3://cool-bucket/rad-project/tubular_data.csv"
        timestamp = '20190307204233'
        test_df_with_md = ingest.set_initial_metadata(df, s3_url, timestamp)
        expected_df = pd.DataFrame([['hello', s3_url, timestamp], ['world', s3_url, timestamp]],
            columns=['werds', '__metadata_original_s3_url', '__metadata_ingest_timestamp'])

        assert df.equals(expected_df)

    def test_initial_ingest_run(self):
        session, input_contract, output_contract = self.setup_session()
        transform_model = session.query(InitialIngestTransformation).filter(InitialIngestTransformation.id == 1).one()
        t = InitialIngestTransform(input_contract, output_contract, transform_model)

        t.run()
        # Need to have the output_contract.write_with_metadata function defined before this can be tested