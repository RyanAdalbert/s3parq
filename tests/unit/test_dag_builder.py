from airflow import DAG
from mock import patch, PropertyMock, MagicMock
import pytest
from core.models.configuration import Pipeline
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
import core.airflow.dagbuilder.dag_builder as dag_builder


@patch('core.airflow.dagbuilder.dag_builder.SessionHelper.get_session', autospec=True )
class Test:

    def setup(self):
        mock_config = CMock()
        mock_config.generate_mocks()
        return mock_config.get_session()

    def test_get_active_pipelines(self, helper_session):
        helper_session.return_value = self.setup()

        dbuilder = dag_builder.DagBuilder()
        pipelines = dbuilder._get_pipelines()

        ## make sure we get a list of Pipelines back
        assert all(isinstance(x, Pipeline) for x in pipelines)
        
        ## make sure they are all active
        assert all(x.is_active for x in pipelines)
        
    def test_get_all_pipelines(self, helper_session):
        helper_session.return_value = self.setup()

        dbuilder = dag_builder.DagBuilder()
        pipelines = dbuilder._get_pipelines(only_active=False)
            
        ## make sure we get a list of Pipelines back
        assert all(isinstance(x, Pipeline) for x in pipelines)
        
        ## make sure there is at least one inactive
        assert False == min([x.is_active for x in pipelines])


    def test_do_build_dags(self, helper_session):
        helper_session.return_value = self.setup()
        dbuilder = dag_builder.DagBuilder()
        dbuilder.do_build_dags()

        assert all(isinstance(x,DAG) for x in dbuilder.dags)

