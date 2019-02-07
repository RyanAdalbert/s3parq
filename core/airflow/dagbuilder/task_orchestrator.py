from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from core.models.configuration import Pipeline
from operator import attrgetter
from core.airflow.plugins.transform_operator import TransformOperator


class TaskOrchestrator:
    
    def __init__(self, pipeline: Pipeline=None, dag:DAG=None)->None: 
        self._pipeline = pipeline
        self._dag = dag
        self._tasks = []

    @property
    def dag(self)->DAG:
        return self._dag

    @dag.setter
    def dag(self,dag:DAG)->None:
        self._dag = dag

    @property
    def tasks(self):
        return self._tasks

    @property
    def pipeline(self):
        return self._pipeline

    @pipeline.setter
    def pipeline(self, pipeline:Pipeline)->None:
        self._pipeline = pipeline 

    @tasks.setter
    def tasks(self, tasks:list)->None:
        raise ValueError('TaskOrchestrator.tasks must not be set directly.')
   
    def do_orchestrate(self)->None:
        if not self._pipeline:
            raise ValueError("TaskOrchestrator cannot run do_orchstrate without a pipeline set.")

        all_pipeline_tasks = []
        for state in self._pipeline.pipeline_states:  
            transformations = self._order_transformations_within_group(state.transformations)
            
            all_transforms = []
            for transformation_group in transformations:
                converted_set = set()
                for transform in transformation_group:
                    to = TransformOperator(transform.id)
                    converted_set.add(to)
                all_transforms.append(tuple([state.pipeline_state_type.name, converted_set]))
            all_pipeline_tasks +=  all_transforms               
        self._tasks = self._apply_deps_to_ordered_tasks(all_pipeline_tasks, self._dag)    
        
## PRIVATE ##


    def _order_transformations_within_group(self, transformations:list)->list:
        """ takes a list of configuration transformations from the same pipeline state, returns them in a list of ordered sets."""
        transformations = sorted(transformations, key=attrgetter('graph_order'))  
        ordered_transformation_groups = [set()]
        graph_cursor = 0
        list_cursor = 0          
        for t in transformations:
            if t.graph_order == graph_cursor:
                ordered_transformation_groups[list_cursor].add(t)
            else:
                list_cursor =+1
                graph_cursor = t.graph_order
                ordered_transformation_groups.append({t})
        return ordered_transformation_groups                       

    def _apply_deps_to_ordered_tasks(self, task_groups:list, dag:DAG)->tuple:
        """ takes an ordered list of tuples. each tuple is (state_name, {set_of_operator_tasks}). Assigns deps to each set for all tasks in the previous set.
            Example: 
                -if ordered_task_sets is: 
                    [{task_1,task2}, {task_3,task_4}, {task_5}]
                this will return a tuple (task_1, task_2, task_3...) where task_1 and task_2 have no upstream, task_3 and task_4 have both task_1 and task_2 as their upstreams, and task_5 will have both task_3 and task_4 as its upstream. 
            RETURNS: tuple of tasks with deps applied
        """  


        spacers =[] 

        def make_spacer(id:int, state_name:str, dag:DAG)->DummyOperator:
            """ look for an existing spacer. return it. if not, make it and return that."""
            spacer_format = f"{state_name}_group_step_{id}"
            if len(spacers) > 0:
                for spacer in spacers:
                    if spacer.task_id == spacer_format:
                        return spacer
            spacer = DummyOperator(task_id=spacer_format)
            spacer.dag=dag  
            spacer.depends_on_past = True
    
            return spacer


        ## first make the spacer operators
        for index, packed_task_group in enumerate(task_groups):
            state_name = packed_task_group[0]
            spacer = make_spacer(index,state_name,dag)
            spacers.append(spacer)

        prepaired_tasks = []
        
        ## now set up/downstreams to the tasks and spacers
        for index, packed_task_group in enumerate(task_groups):
            task_group = packed_task_group[1]
                
            for task in task_group:
                task.dag = dag
                task.depends_on_past = True
                spacers[index] >> task 
                if index < len(spacers) -1:
                    task >> spacers[index +1] 
                prepaired_tasks.append(task)
        
        prepaired_tasks += spacers

        return tuple(prepaired_tasks)    
