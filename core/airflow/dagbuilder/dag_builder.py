from airflow import DAG
from core.models.configuration import Pipeline
from core.helpers.session_helper import SessionHelper
from datetime import datetime, timedelta
from core.airflow.dagbuilder.task_orchestrator import TaskOrchestrator

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
        """Integrates all the components of getting dags, setting task deps etc."""
        self._pipelines = self._get_pipelines()
        sets = self._create_dag_sets(self._pipelines)
        for pipeline, dag in sets:
            tasks = self._get_prepped_tasks(pipeline)
            self._apply_dag_to_tasks(dag, tasks)
            self._dags.append(dag)

    @property
    def dags(self)->list:
        return self._dags

    @dags.setter
    def dags(self,dags)->None:
        self._dags = dags        

    def _create_dag_sets(self, pipelines: list)-> list:
        """ creates a dag for each pipeline
            RETURNS a list of tuples, each containing:
                - the original pipeline object
                - the matching DAG for that pipeline"""
        dags = []
        for pipe in pipelines:
            
            dags.append((pipe, DAG(pipe.name, default_args = self.DEFAULT_ARGS, schedule_interval=f'@{pipe.run_frequency}'),))
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

    def _get_prepped_tasks(self, pipeline: Pipeline)-> tuple:
        """returns a tuple of tasks with deps already applied."""
        to = TaskOrchestrator(pipeline)
        to.do_orchestrate()
        return to.tasks

    def _apply_dag_to_tasks(self, dag:DAG, tasks: tuple)->tuple:
        """returns a tuple of tasks with the dag applied."""
        for task in tasks:
            task.dag = dag
        return tasks

