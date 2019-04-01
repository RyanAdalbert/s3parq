import pytest
import core.models.configuration as config
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
from datetime import datetime

@pytest.fixture
def wrapper():
    mock = CMock()
    mock.generate_mocks()
    yield mock.get_session()
    mock.session.close()

def test_variables_rendered(wrapper):
    session = wrapper
    session.add(config.TransformationTemplate(id=1000, name = "transformapalooza", variable_structures = '''{"name":{"datatype":"string","description":"the name of the agent"}, 
"age":{"datatype":"int", "description":"the integer age of the agent"},
"birthdate":{"datatype":"date","description":"the day this record was born"}}'''))
    session.add(config.Transformation(id = 1000, graph_order = 0, transformation_template_id = 1000, pipeline_state_id=1))
    session.add(config.TransformationVariable(transformation_id=1000, name='name', value='big_test'))
    session.add(config.TransformationVariable(transformation_id=1000, name='age', value='23'))
    session.add(config.TransformationVariable(transformation_id=1000, name='birthdate', value='2018-10-11 10:24:01'))
    session.commit()

    transform = session.query(config.Transformation).filter(config.Transformation.id==1000).one()

    assert transform.variables.name == 'big_test'
    assert transform.variables.age == 23
    assert transform.variables.birthdate == datetime(2018,10,11,10,24,1)
