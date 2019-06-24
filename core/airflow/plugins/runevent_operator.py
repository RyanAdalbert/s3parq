from airflow.operators.python_operator import PythonOperator
from core.helpers.session_helper import SessionHelper
from core.helpers.docker import get_core_job_def_name
from airflow.contrib.hooks.ssh_hook import SSHHook
import core.models.configuration as config
from core.logging import get_logger

def RunEvent_task(pipeline_id: int, **kwargs):
    """
    Increments the run_event table id by one and returns the event as an xcom
    """
    session = SessionHelper().session
    run_event = config.RunEvent(pipeline_id=pipeline_id)
    session.add(run_event)
    session.commit()
    run_id = run_event.id
    session.close()
    kwargs['ti'].xcom_push(key="run_id", value=run_id) 
