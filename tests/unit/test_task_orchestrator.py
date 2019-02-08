import pytest
from core.airflow.dagbuilder.task_orchestrator import TaskOrchestrator
from core.airflow.plugins.transform_operator import TransformOperator
from airflow import DAG
from datetime import datetime
from core.models.configuration import PharmaceuticalCompany, Brand, Pipeline, PipelineType, Segment, PipelineState, PipelineStateType, TransformationTemplate, Transformation
from core.helpers.configuration_mocker import ConfigurationMocker as CMock


class Names:
    cname, bname, ptname, sname, pname, pstname, tname = 'test_client', 'test_brand', 'test_edo_pipeline', 'test_segment', 'test_pipeline', 'test_pipeline_state', 'test_transform_template'


class Test:

    def setup_mock(self):
        mock = CMock()
        session = mock.get_session()
        n = Names()
        session.add(PharmaceuticalCompany(
            id=1, display_name=n.cname, name=n.cname))
        session.add(Brand(id=1, pharmaceutical_company_id=1,
                          display_name=n.bname, name=n.bname))
        session.add(Segment(id=1, name=n.sname))
        session.add(PipelineType(id=1, segment_id=1, name=n.ptname))
        session.add(Pipeline(id=1, pipeline_type_id=1,
                             brand_id=1, name=n.pname))
        session.add(PipelineStateType(id=1, name=n.pstname))
        session.add(PipelineState(id=1, pipeline_state_type_id=1,
                                  graph_order=1, pipeline_id=1))
        session.add(TransformationTemplate(id=1, name=n.tname))
        session.commit()
        return session

    def setup_in_state_transforms(self):
        session = self.setup_mock()
        # Now for the in-state transforms
        session.add(Transformation(id=1, graph_order=0,
                                   transformation_template_id=1, pipeline_state_id=1))
        session.add(Transformation(id=2, graph_order=0,
                                   transformation_template_id=1, pipeline_state_id=1))
        session.add(Transformation(id=3, graph_order=1,
                                   transformation_template_id=1, pipeline_state_id=1))
        session.add(Transformation(id=4, graph_order=1,
                                   transformation_template_id=1, pipeline_state_id=1))
        session.add(Transformation(id=5, graph_order=2,
                                   transformation_template_id=1, pipeline_state_id=1))
        session.commit()
        return session

    def test_order_transformations_within_group(self):
        session = self.setup_in_state_transforms()
        transformations = session.query(Transformation).filter(
            Transformation.pipeline_state_id == 1)

        to = TaskOrchestrator()
        ordered_groups = to._order_transformations_within_group(
            transformations)
        assert len(ordered_groups) == 3

        for x in range(0, 3):
            for t in ordered_groups[x]:
                assert t.graph_order == x, f"graph order incorrect for set number {x}"

    def test_assign_deps_to_ordered_tasks(self):
        dag = DAG("test_dag", start_date=datetime(
            2000, 6, 1), schedule_interval="@daily")
        ordered_transform_operators = [tuple(["raw", {TransformOperator(1), TransformOperator(2)}]),
                                       tuple(
                                           ["ingest", {TransformOperator(3), TransformOperator(4)}]),
                                       tuple(["ingest", {TransformOperator(5)}])]
        to = TaskOrchestrator()

        dep_assigned_tasks = to._apply_deps_to_ordered_tasks(
            ordered_transform_operators, dag)

        # make sure groupings are created
        raw_group_step_0_exists = False

        # make sure downstreams set
        for task in dep_assigned_tasks:
            if task.task_id == "raw_group_step_0":
                raw_group_step_0_exists = True
                assert len(task.downstream_list) == 2

        assert raw_group_step_0_exists

    def test_do_orchestrate(self):
        session = self.setup_in_state_transforms()
        to = TaskOrchestrator()
        pipe = session.query(Pipeline).filter(Pipeline.id == 1).one()
        dag = DAG("test_dag", start_date=datetime(
            2000, 6, 1), schedule_interval="@daily")
        to.dag = dag
        to.pipeline = pipe

        to.do_orchestrate()
        tasks = []
        for state in pipe.pipeline_states:
            for transform in state.transformations:
                tasks.append(transform)

        # same number of tasks: in the case of id==1, we get 3 extra tasks that are state grouping tasks
        assert len(to.tasks) == len(tasks) + 3
