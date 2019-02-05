from airflow.operators import BaseOperator
from airflow.operators.bash_operator import BashOperator

class TransformOperator(BashOperator):
    """ Placeholder for Rayne's class"""

    
    def __init__(self,id:int)->None:
        super().__init__(bash_command='ls', task_id=f'super_task_{id}')
        
       
