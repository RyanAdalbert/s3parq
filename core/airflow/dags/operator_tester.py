from core.constants import ENVIRONMENT
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
### Import the operator you want to test here! ###

if ENVIRONMENT == "dev":

    DEFAULT_ARGS  = {
    "owner": "integrichain",
    "depends_on_past": True,
    "start_date": datetime(2015, 6, 1),
    "email": ["test_dag@integrichain.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5)
    }

    dag = DAG('development_dag_for_testing_operator', default_args = DEFAULT_ARGS, schedule_interval = None)


kickoff_task = DummyOperator("task_that_does_nothing", dag = dag)

### your task with your operator goes here! 
## my_task = MyOperator(task_id = <something>, dag = dag)

### put them in order
## kickoff_task >> my_task
