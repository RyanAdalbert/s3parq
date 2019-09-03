from core.airflow.dagbuilder.dag_builder import DagBuilder
from airflow import DAG
from os import path
from time import sleep

# Only run dag builder if pause_executor file is not present
while path.exists("/root/airflow/dags/pause_executor") == True:
    # TODO: Consider replacing this message with proper logging
    print("executor.py is paused because pause_executor file is present.. rechecking in 10 seconds")
    sleep(10)

dag_builder = DagBuilder()

dag_builder.do_build_dags()

for index, dag in enumerate(dag_builder.dags):
    globals()[f'dag_{index}'] = dag
