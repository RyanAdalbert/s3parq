import pytest
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
import core.models.configuration as config


def test_mock_extract_configurations():
    db = CMock()
    db.generate_mocks()
    session = db.get_session()
    ec = config.ExtractConfiguration

    # depends on hard-coded values in mocker
    q = session.query(ec).filter(ec.id == 2)
    assert q[0].filesystem_path == 'banana_stand'


def test_mock_transformation_relationships():
    db = CMock()
    db.generate_mocks()
    session = db.get_session()
    t = config.Transformation

    # depends on hard-coded values in mocker
    q = session.query(t).filter(t.id == 1)
    secrets = []
    for v in q:
        for row in v.extract_configurations:
           secrets.append(row.secret_name)
    
    assert len(secrets) == 3

    assert set(secrets) == set(['sitwell'])

