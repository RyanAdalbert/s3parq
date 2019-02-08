from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from core.models.configuration import Pipeline
from operator import attrgetter
from core.airflow.plugins.transform_operator import TransformOperator
from core.logging import LoggerMixin


class TaskOrchestrator(LoggerMixin):

    def __init__(self, pipeline: Pipeline = None, dag: DAG = None)->None:
        self._pipeline = pipeline
        self._dag = dag
        self._tasks = []

    @property
    def dag(self)->DAG:
        return self._dag

    @dag.setter
    def dag(self, dag: DAG)->None:
        self._dag = dag

    @property
    def tasks(self):
        return self._tasks

    @property
    def pipeline(self):
        return self._pipeline

    @pipeline.setter
    def pipeline(self, pipeline: Pipeline)->None:
        self._pipeline = pipeline

    @tasks.setter
    def tasks(self, tasks: list)->None:
        error_messge = 'TaskOrchestrator.tasks must not be set directly.'
        self.logger.critical(error_message)
        raise ValueError(error_message)

    def do_orchestrate(self)->None:
        self.logger.info("Begin orchestrating tasks...")
        if not (self._pipeline and self._dag):
            except_message = "TaskOrchestrator cannot run do_orchstrate without a pipeline and a dag set."
            self.logger.critical(except_message)
            raise ValueError(except_message)

        all_pipeline_tasks = []
        for state in self._pipeline.pipeline_states:
            self.logger.debug(
                f"Ordering transforms in state {state.pipeline_state_type.name}...")
            transformations = self._order_transformations_within_group(
                state.transformations)
            self.logger.debug(
                f"Done ordering transforms for state {state.pipeline_state_type.name}. {len(transformations)} sets of transforms created.")
            all_transforms = []
            for transformation_group in transformations:
                converted_set = set()
                for transform in transformation_group:
                    to = TransformOperator(transform.id)
                    converted_set.add(to)
                all_transforms.append(
                    tuple([state.pipeline_state_type.name, converted_set]))
            all_pipeline_tasks += all_transforms
        self.logger.debug(
            f"Applying dependancies to tasks for dag {self._dag.dag_id}...")
        self._tasks = self._apply_deps_to_ordered_tasks(
            all_pipeline_tasks, self._dag)
        self.logger.info(
            f"Done orchestrating tasks. {len(self._tasks)} orchestrated.")

## PRIVATE ##

    def _order_transformations_within_group(self, transformations: list)->list:
        """ takes a list of configuration transformations from the same pipeline state, returns them in a list of ordered sets."""
        transformations = sorted(
            transformations, key=attrgetter('graph_order'))
        ordered_transformation_groups = [set()]
        graph_cursor = 0
        list_cursor = 0
        for t in transformations:
            if t.graph_order == graph_cursor:
                ordered_transformation_groups[list_cursor].add(t)
            else:
                list_cursor = +1
                graph_cursor = t.graph_order
                ordered_transformation_groups.append({t})
            self.logger.debug(
                f"added task with graph order # {t.graph_order} to group {graph_cursor}")
        return ordered_transformation_groups

    def _apply_deps_to_ordered_tasks(self, task_groups: list, dag: DAG)->tuple:
        """ takes an ordered list of tuples. each tuple is (state_name, {set_of_operator_tasks}). Assigns deps to each set for all tasks in the previous set.
            Example: 
                -if ordered_task_sets is: 
                    [("raw",{task_1,task2},),("raw", {task_3,task_4},), ("ingest",{task_5},)]
                this will return a tuple (raw_group_task_1, raw_group_task_2, task_1, task_2, task_3...) where task_1 and task_2 depend on upstream raw_group_1 and downstream raw_group_2, task_3 and task_4 have upstream raw_group_2 and downstream ingest_group_1 etc. 
            RETURNS: tuple of tasks with deps applied
        """

        spacers = []

        def make_spacer(id: int, state_name: str, dag: DAG)->DummyOperator:
            """ look for an existing spacer. return it. if not, make it and return that."""

            spacer_format = f"{state_name}_group_step_{id}"
            if len(spacers) > 0:
                for spacer in spacers:
                    if spacer.task_id == spacer_format:
                        return spacer
            spacer = DummyOperator(task_id=spacer_format)
            spacer.dag = dag
            spacer.depends_on_past = True

            return spacer

        # first make the spacer operators
        for index, packed_task_group in enumerate(task_groups):
            state_name = packed_task_group[0]
            spacer = make_spacer(index, state_name, dag)
            spacers.append(spacer)

        self.logger.debug(f"Created {len(spacers)} spacer tasks.")
        prepaired_tasks = []

        # now set up/downstreams to the tasks and spacers
        for index, packed_task_group in enumerate(task_groups):
            task_group = packed_task_group[1]

            for task in task_group:
                task.dag = dag
                task.depends_on_past = True
                self.logger.debug(
                    f"Set downstream on {spacers[index].task_id} to {task.task_id}.")
                spacers[index] >> task
                if index < len(spacers) - 1:
                    self.logger.debug(
                        f"Set downstream on {task.task_id} to {spacers[index + 1].task_id}.")
                    task >> spacers[index + 1]
                prepaired_tasks.append(task)

        prepaired_tasks += spacers

        return tuple(prepaired_tasks)
