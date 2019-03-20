import pytest
from datetime import datetime
from core.models.configuration import PharmaceuticalCompany, Brand, Pipeline, PipelineType, Segment, PipelineState, \
    PipelineStateType, TransformationTemplate, Transformation, ExtractTransformation, InitialIngestTransformation
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
from sqlalchemy.orm import with_polymorphic


class Names:
    cname, bname, ptname, sname, pname, pstname, tname = 'test_client', 'test_brand', 'test_edo_pipeline', 'test_segment', 'test_pipeline', 'test_pipeline_state', 'extract_from_ftp'


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
        session.add(TransformationTemplate(id=2, name="initial_ingest"))

        session.commit()
        return session

    def setup_in_state_transforms(self):
        session = self.setup_mock()
        # Now for the in-state transforms
        session.add(ExtractTransformation(id=1, graph_order=0,
                                          transformation_template_id=1, pipeline_state_id=1))
        session.add(Transformation(id=2, graph_order=0,
                                   transformation_template_id=2, pipeline_state_id=1))
        session.add(Transformation(id=3, graph_order=1,
                                   transformation_template_id=2, pipeline_state_id=1))
        session.add(Transformation(id=4, graph_order=1,
                                   transformation_template_id=2, pipeline_state_id=1))
        session.add(Transformation(id=5, graph_order=2,
                                   transformation_template_id=2, pipeline_state_id=1))
        session.commit()
        return session

    def test_order_transformations_within_group(self):
        session = self.setup_in_state_transforms()

        t_polymorphic = with_polymorphic(Transformation, '*')

        transformations = session.query(t_polymorphic).filter(
            Transformation.pipeline_state_id == 1)

        first = transformations[0]
        assert (hasattr(first, 'extract_configurations'))
        assert (isinstance(first, ExtractTransformation))

        second = transformations[1]
        assert (not hasattr(second, 'extract_configurations'))
        assert (isinstance(second, InitialIngestTransformation))
