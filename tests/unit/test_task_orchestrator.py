import pytest
from core.airflow.dagbuilder.task_orchestrator import TaskOrchestrator
from core.models.configuration import PharmaceuticalCompany, Brand, Pipeline, PipelineType, Segment, PipelineState, PipelineStateType, TransformationTemplate, Transformation
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
from sqlalchemy import or_

class Names:
    cname, bname, ptname, sname, pname, pstname, tname = 'test_client', 'test_brand', 'test_edo_pipeline', 'test_segment','test_pipeline', 'test_pipeline_state', 'test_transform_template'

class Test:

    def setup_mock(self):
        mock = CMock()
        session = mock.get_session()
        n = Names()
        session.add(PharmaceuticalCompany(id=1, display_name=n.cname, name=n.cname))
        session.add(Brand(id=1, pharmaceutical_company_id=1, display_name=n.bname, name=n.bname))
        session.add(Segment(id=1, name=n.sname))
        session.add(PipelineType(id=1, segment_id=1,name=n.ptname))
        session.add(Pipeline(id=1, pipeline_type_id=1, brand_id=1, name=n.pname))
        session.add(PipelineStateType(id=1, name=n.pstname))
        session.add(PipelineState(id=1, pipeline_state_type_id=1, graph_order=1, pipeline_id=1))
        session.add(TransformationTemplate(id=1,name=n.tname))
        session.commit()
        return session


    def setup_in_state_transforms(self):
        session = self.setup_mock()
        n = Names()
        ### Now for the in-state transforms
        session.add(Transformation(id=1, graph_order=0, transformation_template_id=1, pipeline_state_id=1))
        session.add(Transformation(id=2, graph_order=0, transformation_template_id=1, pipeline_state_id=1))
        session.add(Transformation(id=3, graph_order=1, transformation_template_id=1, pipeline_state_id=1))
        session.add(Transformation(id=4, graph_order=1, transformation_template_id=1, pipeline_state_id=1))
        session.add(Transformation(id=5, graph_order=2, transformation_template_id=1, pipeline_state_id=1))
        session.commit()
        return session


    def test_order_tasks_within_group(self):
        session = self.setup_in_state_transforms()
        transformations = session.query(Transformation).filter(Transformation.pipeline_state_id==1)
        
        to = TaskOrchestrator()
        ordered_groups = to._order_tasks_within_group(transformations)        
        assert len(ordered_groups) == 3
        
        for x in range(0,3):
            for t in ordered_groups[x]:
                assert t.graph_order == x, f"graph order incorrect for set number {x}"

    
    ## TODO: patch transform operator here
    def test_assign_deps_to_ordered_groups(self):
        session = self.setup_in_state_transforms()
        n = Names()
        ordered_transforms = [  set(session.query(Transformation).filter(or_(Transformation.id==1, Transformation.id==2))), 
                                set(session.query(Transformation).filter(or_(Transformation.id==3, Transformation.id==4))),
                                set(session.query(Transformation).filter(Transformation.id==4))]
        to = TaskOrchestrator()
        dep_assigned_tasks = to._apply_deps_to_ordered_tasks(ordered_transforms)        

        task_id_format = f'{n.pname}_{n.pstname}_{n.tname}_'
                
        pass
        #for task in dep_assigned_tasks:



    def test_do_orchestrate(self):
        pass

    '''



    def test_build_dag_tasks_builds_tasks(self, helper_session):
        transformations = [ MagicMock(  id=100,
                                        transformation_template_id=100,
                                        pipeline_state_id=2,
                                        graph_order=0),
                            MagicMock(  id=100,
                                        transformation_template_id=100,
                                        pipeline_state_id=2,
                                        graph_order=1)]
        
        dbuilder = dag_builder.DagBuilder()
        tasks = dbuilder._build_tasks(pipeline, dag)

        assert all(isinstance(x, TransformationOperator for x in tasks))

    def test_
        
    

        assert all(isinstance(x, DAG) for x in dags)

    def test_orchestrator_deps_inside_state(self):
        session = self.setup_mock()

        pipeline = session.query(Pipeline).first()
        to = TaskOrchestrator(Pipeline)
        tasks = to.tasks        
        
        ## test downstreams
        graph_0_downstream = []
        graph_1_downstream = []
        graph_2_downstream = []
        task_id_format = f'{n.pname}_{n.pstname}_{n.tname}_'
            
        ## make sure we get 5 tasks back
        assert len(tasks) == 5, f"Expected 5 tasks, got {len(tasks)} back."

        for t in tasks:
            if t.task_id == task_id_format+'1' or t.task_id == task_id_format+'2': 
                for d in t.downstream_list:
                    graph_0_downstream.append(d.task_id)
                assert set(graph_0_downstream) == set(3,4)
            elif t.task_id == task_id_format+'3' or t.task_id == task_id_format+'4':
                for d in t.downstream_list:
                    graph_1_downstream.append(d.task_id)
                assert set(graph_1_downstream) == set(5)
            elif t.task_id == task_id_format+'5':
                for d in t.downstream_list:
                    graph_2_downstream.append(d.task_id)
                assert set(graph_2_downstream) == set()
            else:
                pytest.fail('Task name is improperly formatted')
       '''
