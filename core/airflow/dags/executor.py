from core.airflow.dagbuilder.dag_builder import DagBuilder
from airflow import DAG

dag_builder = DagBuilder()

dag_builder.do_build_dags()

for index, dag in enumerate(dag_builder.dags):
    globals()[f'dag_{index}'] = dag
