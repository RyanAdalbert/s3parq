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

class Test:
    def setup_session(self):
        session = setup_base_session()
        session.add(PipelineStateType(id=1, name='ingest'))
        session.add(PipelineState(id=1, pipeline_state_type_id=1,
                                  graph_order=1, pipeline_id=1))
        session.add(TransformationTemplate(id=1, name='initial_ingest'))
        session.add(InitialIngestTransformation(id=1, graph_order=0, transformation_template_id=1, pipeline_state_id=1))
        session.commit()
        return session

    def test_ingest_validate_config(self):
        session = self.setup_session()
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