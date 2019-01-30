import pytest
import core.models.configuration as config
from core.helpers.configuration_mocker import ConfigurationMocker as CMock


def test_get_extract_configuration():
    session = CMock().get_session()
    # augment the helper data. TODO: build out independent coverage w/o the helper.
    CMock().generate_mocks()
    # make dummy records
    ec = config.ExtractConfiguration
    t = config.Transformation
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

    q = session.query(t).filter(t.id == 100)
    secrets = []
    for f_transform in q:
        for extract in f_transform.extract_configurations:
            secrets.append(extract.secret_name)

    assert set(test_secret_names) == set(secrets)
