from airflow import DAG
from core.models.configuration import Pipeline
from core.helpers.session_helper import SessionHelper
from datetime import datetime, timedelta


class DagBuilder:

    DEFAULT_ARGS = {
    "owner": "integriChain",
    "depends_on_past": False,
    "start_date": datetime(2000, 1, 1),
    "email": ["engineering@integrichain.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
    }

    def do_build_dags(self)->None:
        """Integrates all the components of getting dags."""
        self.__pipelines = self._get_pipelines()
        self.__dags = self._create_dags(self.__pipelines)

    def _create_dags(self, pipelines: list)-> list:
        """ creates a dag for each pipeline
            RETURNS a list of airflow dag objects"""
        dags = []
        for index, pipe in enumerate(pipelines):
            dags.append(DAG(pipe.name, default_args = self.DEFAULT_ARGS, schedule_interval=f'@{pipe.run_frequency}'))
        return dags                     


    def _get_pipelines(self, only_active:bool = True) -> list:
        """ gets all the pipelines from the configuration session.
            ARGS
                - only_active: if true ignore inactive pipelines
            RETURNS list of core.model.Pipeline objects
        """
        session = SessionHelper().get_session()

        if only_active:
            pipelines = session.query(Pipeline).filter(Pipeline.is_active)
        else:
            pipelines = session.query(Pipeline)
        return pipelines

    def _build_task(self, d   
