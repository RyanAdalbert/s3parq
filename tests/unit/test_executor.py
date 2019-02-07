import pytest
from airflow import DAG

def test_execute():
    global_dag_count = 0
    import core.airflow.dags.executor as executor
    for obj in dir(executor):
        if isinstance(DAG, type(getattr(executor, obj))):
            global_dag_count +=1   
    
    
    assert global_dag_count > 0
