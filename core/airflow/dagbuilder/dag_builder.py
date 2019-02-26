from airflow import DAG
from core.models.configuration import Pipeline
from core.helpers.session_helper import SessionHelper
from datetime import datetime, timedelta
from core.airflow.dagbuilder.task_orchestrator import TaskOrchestrator
from core.logging import LoggerMixin


class DagBuilder(LoggerMixin):

    def __init__(self):
        self._dags = []
        self.DEFAULT_ARGS = {
            "owner": "integriChain",
            "depends_on_past": False,
            "start_date": datetime(2019, 2, 24),
            "email": ["engineering@integrichain.com"],
            "email_on_failure": False,
            "email_on_retry": False,
            "retries": 1,
            "retry_delay": timedelta(minutes=5)
        }

    def do_build_dags(self)->None:
        """Integrates all the components of getting dags, setting task deps etc."""
        self.logger.info('Beginning run to build all dags...')

        self._pipelines = self._get_pipelines()
        sets = self._create_dag_sets(self._pipelines)
        for pipeline, dag in sets:
            tasks = self._get_prepped_tasks(pipeline, dag)
            self._dags.append(dag)
        self.logger.info(f"Done with run. {len(self._dags)} dags built.")

    @property
    def dags(self)->list:
        return self._dags

    @dags.setter
    def dags(self, dags)->None:
        self._dags = dags

    def _create_dag_sets(self, pipelines: list)-> list:
        """ creates a dag for each pipeline
            RETURNS a list of tuples, each containing:
                - the original pipeline object
                - the matching DAG for that pipeline"""
        dags = []
        self.logger.debug("Creating DAGs from pipelines...")
        for pipe in pipelines:
            self.logger.debug(f"Created DAG {pipe.name}")
            dags.append((pipe, DAG(pipe.name,
                                   default_args=self.DEFAULT_ARGS,
                                   # airflow may no longer support start_date in default_args
                                   start_date=self.DEFAULT_ARGS['start_date'],
                                   schedule_interval=f'@{pipe.run_frequency}'),))
            self.logger.debug("Done creating DAGs.")
        return dags

    def _get_pipelines(self, only_active: bool = True) -> list:
        """ gets all the pipelines from the configuration session.
            ARGS
                - only_active: if true ignore inactive pipelines
            RETURNS list of core.model.Pipeline objects
        """
        self.logger.debug(
            f"getting {'active' if only_active else 'all'} pipelines from config...")
        session = SessionHelper().session

        if only_active:
            pipelines = session.query(Pipeline).filter(Pipeline.is_active)
        else:
            pipelines = session.query(Pipeline)
        self.logger.debug(
            f"Done getting pipelines, {len([x for x in pipelines])} pipelines found.")
        return pipelines

    def _get_prepped_tasks(self, pipeline: Pipeline, dag: DAG)-> tuple:
        """returns a tuple of tasks with deps and dag already applied."""
        to = TaskOrchestrator(pipeline, dag)
        to.do_orchestrate()
        return to.tasks
