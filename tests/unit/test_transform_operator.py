from airflow.models import BashOperator
from airflow import utils as airflow_utils
from core.helpers import session_helper
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
        session.commit()
        return session

    def setup_in_state_transforms(self):
        session = self.setup_mock()
        # Now for the in-state transforms
        session.add(Transformation(id=1, graph_order=0,
                                   transformation_template_id=1, pipeline_state_id=1))
        session.add(Transformation(id=2, graph_order=0,
                                   transformation_template_id=1, pipeline_state_id=1))
        session.commit()
        return session

    def test_run(self):
        # test_to = transform_operator.TransformOperator(transform_id=2)
        pass

    def test_pass_super(self):
        pass

    def test_get_transform_info(self):
        session = self.setup_in_state_transforms()
        pass

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