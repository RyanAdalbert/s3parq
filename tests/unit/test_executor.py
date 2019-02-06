import pytest
from airflow import DAG

def test_execute():
    import core.airflow.dags.executor as executor

    global_dag_count = sum([isinstance(x, DAG) for x in globals()])
    
    assert global_dag_count > 0
