from core.models.configuration import Pipeline
from operator import attrgetter


class TaskOrchestrator:
    
    def __init__(self, pipeline:Pipeline)->None:
        self._pipeline = pipeline
        self._tasks = []
    @property
    def tasks(self):
        return self._tasks

    @tasks.setter
    def tasks(self, tasks):
        raise ValueError('TaskOrchestrator.tasks must not be set directly.')
   
    def _order_tasks_within_group(self, tasks:list)->list:
        """ takes a list of airflow tasks from the same pipeline state, returns them in a list of ordered sets."""
        tasks = sorted(tasks, key=attrgetter('graph_order'))  
        ordered_task_groups = [set()]
        graph_cursor = 0
        list_cursor = 0          
        for t in tasks:
            if t.graph_order == graph_cursor:
                ordered_task_groups[list_cursor].add(t)
            else:
                list_cursor =+1
                graph_cursor = t.graph_order
                ordered_task_groups.append({t})
        return ordered_task_groups                       

    def _apply_deps_to_ordered_tasks(self, tasks:list)->list:
        pass
