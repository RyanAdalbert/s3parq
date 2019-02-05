from core.models.configuration import Pipeline
from operator import attrgetter
from core.airflow.plugins.transform_operator import TransformOperator


class TaskOrchestrator:
    
    def __init__(self, pipeline: Pipeline=None)->None: 
        self._pipeline = pipeline
        self._tasks = []

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
                    converted_set.add(TransformOperator(transform.id))
                all_transforms.append(converted_set)
            all_pipeline_tasks.append(all_transforms)               
         
        self._tasks = self._apply_deps_to_ordered_tasks(all_pipeline_tasks)    
        
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

    def _apply_deps_to_ordered_tasks(self, task_groups:list)->list:
        """ takes an ordered list of sets and assigns deps to each set for all tasks in the previous set.
            Example: 
                -if ordered_task_sets is: 
                    [{task_1,task2}, {task_3,task_4}, {task_5}]
                this will return a tuple (task_1, task_2, task_3...) where task_1 and task_2 have no upstream, task_3 and task_4 have both task_1 and task_2 as their upstreams, and task_5 will have both task_3 and task_4 as its upstream. 
            RETURNS: tuple of tasks with deps applied
        """  
        prepaired_tasks = []
        group_ids =[]
        for index,task_group in enumerate(task_groups):
            group_ids.append([x.task_id for x in task_group])
            if len(group_ids) > 1:
                for task in task_group:
                    task.set_upstream(group_ids[index -1])
                    prepaired_tasks.append(task)
        return tuple(prepaired_tasks)    
