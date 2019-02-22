#from airflow.models import BashOperator
#from airflow import utils as airflow_utils
#from core.helpers import session_helper
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

# from airflow.utils import  apply_defaults
# from airflow.operators.bash_operator import BashOperator
# from git import Repo
# from collections import namedtuple
# from core.contract import Contract
# from core.helpers.project_root import ProjectRoot
# from core.helpers.session_helper import SessionHelper
# import core.models.configuration as config

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
    @patch('core.airflow.plugins.transform_operator.Repo', autoSpec=True)
    def test_transform_operator_sends_to_batch(self,mock_repo,mock_session_helper):
        n = Names()
        type(mock_session_helper.return_value).session = PropertyMock(return_value = self.setup_session_mock())
            
        type(mock_repo.return_value.active_branch.return_value).name = PropertyMock(return_value = "test_branch")
        
        operator = TransformOperator(transform_id=1)
        
        assert operator.task_id == f"{n.pname}_{n.pstname}_{n.tname}_1".lower()






"""

class Names:
    cname, bname, ptname, sname, pname, pstname, tname = 'test_client', 'test_brand', 'test_edo_pipeline', 'test_segment', 'test_pipeline', 'test_pipeline_state', 'test_transform_template'


@patch('core.airflow.plugins.transform_operator.SessionHelper', autospec=True)
@patch('airflow.operators.bash_operator.BashOperator', autospec=True)
class Test:

        # transform = self._get_transform_info()
        # p_name = transform.pipeline_state.pipeline.name
        # p_stname = transform.pipeline_state.pipeline_state_type.name
        # t_name = transform.transformation_template.name
        # task_id = f"{p_name}_{p_stname}_{t_name}_{self.transform_id}".lower()

        # repo = Repo(ProjectRoot().get_path())
        # branch = repo.active_branch.name.lower()

    def setup_mock(self):
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


    def stub_class_under_test(self):
        class stub_obj(object):
            pass
        test_obj = stub_obj()
        test_obj.__class__ = TransformOperator(transform_id=1)
        test_obj.id = 1
        
        return test_obj
 
    def test_get_transform_info(self):
        session = self.setup_mock()
        operator = self.stub_class_under_test()


    def test_generate_task_id(self, helper_session):
        type(helper_session.return_value).session = PropertyMock(
            return_value=self.setup())
        
        
        trans_op = TransformOperator(transform_id=2)
        task_id = trans_op._generate_task_id()

        assert task_id == f"{pname}_{pstname}_{tname}_2".lower()

    def test_generate_contract_params(self):
        pass

    def test_generate_bash_command(self):
        pass

"""   
    

    




