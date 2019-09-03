from core.airflow.dagbuilder.dag_builder import DagBuilder
from airflow import DAG
from os import path
from time import sleep
from core.logging import LoggerSingleton

logger = LoggerSingleton.logger

# Only run dag builder if pause_executor file is not present
while path.exists("/root/airflow/dags/pause_executor") == True:
    logger.info("executor.py is paused because pause_executor file is present.. rechecking in 10 seconds")
    sleep(10)

dag_builder = DagBuilder()

dag_builder.do_build_dags()

for index, dag in enumerate(dag_builder.dags):
    globals()[f'dag_{index}'] = dag
