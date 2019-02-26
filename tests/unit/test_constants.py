import pytest
import core.constants as c


def test_envar_is_constant(monkeypatch):
    test_var = 'tricks are not illusions, Michael.'
    with monkeypatch.context() as m:
        m.setenv('ICHAIN_GOB_BLUTH', test_var)
        c.reset_constants()
        assert c.GOB_BLUTH == test_var


def test_envar_overrides_config_file(monkeypatch):
    test_var = 'no touching!'
    with monkeypatch.context() as m:
        m.setenv('ICHAIN_DEV_BUCKET', test_var)
        c.reset_constants()
        assert c.DEV_BUCKET == test_var


def test_branch_is_prod_for_prod(monkeypatch):
    with monkeypatch.context() as m:
        m.setenv('ICHAIN_ENVIRONMENT', 'prod')
        c.reset_constants()
        assert c.BRANCH_NAME == 'prod'
