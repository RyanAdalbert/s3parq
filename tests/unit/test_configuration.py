import pytest
import core.models.configuration as config
from core.models.configuration import Transformation, ExtractTransformation
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
from sqlalchemy.orm import with_polymorphic

from core.models.configuration import PharmaceuticalCompany, Brand, Pipeline, PipelineType, Segment, PipelineState, \
    PipelineStateType, TransformationTemplate, Transformation, ExtractTransformation, InitialIngestTransformation
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
from sqlalchemy.orm import with_polymorphic


class Names:
    cname, bname, ptname, sname, pname, pstname, tname = 'test_client', 'test_brand', 'test_edo_pipeline', 'test_segment', 'test_pipeline', 'test_pipeline_state', 'extract_from_ftp'


@pytest.fixture
def teardown():
    mock = CMock()
    yield 
    mock.purge()
    



def setup_mock():
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

def setup_in_state_transforms():
    session = setup_mock()
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

def test_get_extract_configuration():
    session = setup_in_state_transforms()

     # make dummy records
    ec = config.ExtractConfiguration
    t = config.ExtractTransformation
    polymorphic_t = with_polymorphic(Transformation, [ExtractTransformation])
    session.add(t(id=100, pipeline_state_id=1, transformation_template_id=1))
    session.commit()

    test_secret_names = []
    for x in range(0, 3):
        sname = f'test_secret_{x}'
        session.add(ec(transformation_id=100,
                       secret_type_of="FTP",
                       secret_name=sname))
        test_secret_names.append(sname)

    session.commit()

    q = session.query(polymorphic_t).filter(t.id == 100)
    
    print(q)
    secrets = []
    for f_transform in q:
        print(f_transform)
        for extract in f_transform.extract_configurations:
            secrets.append(extract.secret_name)

    assert set(test_secret_names) == set(secrets)
