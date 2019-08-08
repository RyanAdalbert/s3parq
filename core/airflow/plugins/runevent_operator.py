from airflow.operators.python_operator import PythonOperator
from core.helpers.session_helper import SessionHelper
from core.models.configuration import RunEvent

def RunEvent_task(pipeline_id: int, **kwargs):
    """
    Increments the run_event table id by one and returns the event as an xcom
    """
    session = SessionHelper().session
    run_event = RunEvent(pipeline_id=pipeline_id)
    session.add(run_event)
    session.commit()
    run_id = run_event.id
    session.close()
    kwargs['ti'].xcom_push(key="run_id", value=run_id) 
