import pytest
import core.helpers.pipeline_builder as pb
from core.helpers.session_helper import SessionHelper
import core.models.configuration as config
import random
import string


def rand_string()->str:
    return "".join([random.choice(string.ascii_lowercase) for _ in range(random.randint(10,25))])

def test_new_build():
    session = SessionHelper().session
    tr_id = pb.build("foo", "bar", "new_state", "new_transform", session)[0]
    tr = session.query(config.Transformation).filter_by(id=tr_id).one()
    assert tr.transformation_template.name == "new_transform"
    session.close()

def test_get_or_create_exists():
    session = SessionHelper().session
    expected = session.query(config.PharmaceuticalCompany).filter_by(id=1).one().name
    find = dict(id=1)
    co = pb._get_or_create(session, config.PharmaceuticalCompany, find)
    assert co.name == expected
    session.close()

def test_get_or_create_not_exists():
    session = SessionHelper().session
    test_id = 1000000000
    find = dict(id=test_id, name="bananaco", display_name="bananaco")
    co = pb._get_or_create(session, config.PharmaceuticalCompany, find)
    assert co.id == test_id
    assert co.name == "bananaco"
    session.close()
