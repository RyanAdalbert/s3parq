from airflow import DAG
from mock import patch, PropertyMock
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

    def test_create_dags_builds_all_dags(self, helper_session):
        pipeline_mocks = [ MagicMock(name="pipe1",
                            id=12,
                            run_frequency="daily"),
                          MagicMock(name="pipe2",
                          id=24,
                          run_frequency="daily")]
                              
        dbuilder = dag_builder.DagBuilder()
        dags = dbuilder._create_dags(pipeline_mocks)
        
        assert all(isinstance(x, DAG) for x in dags)

    def test_build_dag_tasks_builds_tasks(self, helper_session):
        transformations = [ MagicMock(  id=100,
                                        transformation_template_id=100,
                                        pipeline_state_id=2,
                                        graph_order=0),
                            MagicMock(  id=100,
                                        transformation_template_id=100,
                                        pipeline_state_id=2,
                                        graph_order=1)]
        
        dbuilder = dag_builder.DagBuilder()
        dags = dbuilder._build_tasks(pipeline, dag)
        
        assert all(isinstance(x, DAG) for x in dags)
