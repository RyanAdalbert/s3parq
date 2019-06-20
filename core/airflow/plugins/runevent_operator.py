from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from airflow.utils.decorators import apply_defaults
from airflow.contrib.operators.python_operator import PythonOperator
from airflow.
from collections import namedtuple
from core.constants import BATCH_JOB_QUEUE, BRANCH_NAME, ENVIRONMENT
from core.contract import Contract
from core.helpers.project_root import ProjectRoot
from core.helpers.session_helper import SessionHelper
from core.helpers.docker import get_core_job_def_name
from airflow.contrib.hooks.ssh_hook import SSHHook
import core.models.configuration as config
from core.logging import get_logger

def get_run_id(**context):
    """
    Increments the run_event table id by one and returns the event as an xcom
    """
    session = SessionHelper().session
    new_run_event = config.RunEvent(pipeline_id=1)
    run_id =session.add(new_run_event)
    session.close()
    task_instance = context['task_instance']
    task_instance.xcom_push(run_id=run_id) 

    