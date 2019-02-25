from core.models.configuration import (
    PharmaceuticalCompany, 
    Brand, 
    Pipeline, 
    PipelineType, 
    Segment, 
    PipelineState, 
    PipelineStateType, 
    TransformationTemplate, 
    Transformation
)
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
from mock import patch, PropertyMock, MagicMock
import pytest

from core.airflow.plugins.transform_operator import TransformOperator

class Names:
    cname, bname, ptname, sname, pname, pstname, tname = 'test_client', 'test_brand', 'test_edo_pipeline', 'test_segment', 'test_pipeline', 'test_pipeline_state', 'test_transform_template'
class Test:

    def setup_session_mock(self):
        mock = CMock()
        session = mock.get_session()
        n = Names()
        session.add(PharmaceuticalCompany(
            id=1, display_name=n.cname, name=n.cname))
        session.add(Brand(id=1, pharmaceutical_company_id=1,
                          display_name=n.bname, name=n.bname))
        session.add(Segment(id=1, name=n.sname))
        session.add(PipelineType(id=1, segment_id=1, name=n.ptname))
        session.add(Pipeline(id=1, pipeline_type_id=1,
                             brand_id=1, name=n.pname))
        session.add(PipelineStateType(id=1, name=n.pstname))
        session.add(PipelineState(id=1, pipeline_state_type_id=1,
                                  graph_order=1, pipeline_id=1))
        session.add(TransformationTemplate(id=1, name=n.tname))

        session.add(Transformation(id=1, graph_order=0,
                                   transformation_template_id=1, pipeline_state_id=1))
        session.add(Transformation(id=2, graph_order=0,
                                   transformation_template_id=1, pipeline_state_id=1))
        session.commit()
        return session


    @patch('core.airflow.plugins.transform_operator.SessionHelper', autospec=True)
    @patch('core.airflow.plugins.transform_operator.BRANCH_NAME')
    def test_transform_operator_sends_to_batch(self,mock_repo,mock_session_helper):
        n = Names()
        type(mock_session_helper.return_value).session = PropertyMock(return_value = self.setup_session_mock())
            
        mock_repo.return_value = PropertyMock(return_value = "test_branch")
        
        operator = TransformOperator(transform_id=1)
        
        assert operator.task_id == f"{n.pname}_{n.pstname}_{n.tname}_1".lower()

