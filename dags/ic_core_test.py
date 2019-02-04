import airflow
from airflow import DAG
from airflow.models import Variable
from datetime import datetime, timedelta
import json
from core.helpers import docker

from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
}

# 9am on Monday (for now)
dag = DAG('ic_core_test', default_args=default_args, schedule_interval='0 10 * * *')

op = BashOperator(
    bash_command="echo 'Hello Human'",
    task_id="test_1",
    dag=dag
)
