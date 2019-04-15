import pytest
from unittest.mock import patch
import os
from sqlalchemy.orm.session import Session
from core.helpers.project_root import ProjectRoot
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
import core.models.configuration as config
from core.helpers.session_helper import SessionHelper
from core.helpers.file_mover import FileMover, FileDestination
from core.helpers.session_helper import SessionHelper


# Project Root Helper
def test_project_root_in_project():
    root = ProjectRoot()
    assert isinstance(root.get_path(), str)
    assert isinstance(root.__str__(), str)


def test_project_root_not_in_project(monkeypatch):
    with monkeypatch.context() as m:
        m.chdir('/')

        # this feels icky. But project root needs the docker path for special cases, so we bake it in here.
        docker_special_path = '/usr/src/app'
        if os.path.isfile(f'{docker_special_path}/setup.py'):
            root = ProjectRoot()
            assert root.get_path() == docker_special_path
        else:
            with pytest.raises(Exception):
                root = ProjectRoot()
                root.get_path()


# Session Helper
@patch('core.constants.ENVIRONMENT')
def test_session_helper_dev(ENV):
    ENV.return_value = "dev"
    session = SessionHelper()
    assert isinstance(session.session, Session)





class secret_mock():
    def __init__(self):
        self.user = 'test_user'
        self.password = 'test_password'
        self.host = 'test_host'
        self.port = 'test_port'
        self.mode = 'test_mode'


@patch('paramiko.Transport')
@patch('paramiko.SFTPClient.from_transport')
def test_filemover_paramiko(paramiko_trans, paramiko_sftp):
    sm = secret_mock()

    with FileMover(sm) as fm:
        assert paramiko_trans.called
        assert paramiko_sftp.called


@patch('paramiko.Transport')
@patch('paramiko.SFTPClient')
def test_get_file_type(paramiko_trans, paramiko_sftp):
    sm = secret_mock()
    fm = FileMover(sm)
    test_file = "test_file_name"

    fd = [FileDestination(regex=".*", file_type="all")]
    ft = fm.get_file_type(test_file, fd)
    assert ft, "all"

    fd = [FileDestination(regex="n^", file_type="none")]
    ft = fm.get_file_type(test_file, fd)
    assert ft, "dont_move"

## SessionHelper

@patch("core.helpers.session_helper.config")
@patch("core.helpers.session_helper.CMock")
@patch("core.helpers.session_helper.ENVIRONMENT","prod")
def test_session_helper_prod(mock_cmock, mock_config):
    session = SessionHelper().session
    assert mock_config.GenerateEngine.called
    assert mock_config.Session.called
    assert not mock_cmock.called

@patch("core.helpers.session_helper.config")
@patch("core.helpers.session_helper.CMock")
@patch("core.helpers.session_helper.ENVIRONMENT","uat")
def test_session_helper_uat(mock_cmock, mock_config):
    session = SessionHelper().session
    assert mock_config.GenerateEngine.called
    assert mock_config.Session.called
    assert not mock_cmock.called

@patch("core.helpers.session_helper.config")
@patch("core.helpers.session_helper.CMock")
@patch("core.helpers.session_helper.ENVIRONMENT","dev")
def test_session_helper_dev(mock_cmock, mock_config):
    session = SessionHelper().session
    assert not mock_config.GenerateEngine.called
    assert mock_cmock.called
