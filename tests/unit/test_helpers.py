import pytest
from unittest.mock import patch
import os
from sqlalchemy.orm.session import Session
from core.helpers.project_root import ProjectRoot
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
import core.models.configuration as config
from core.helpers.session_helper import SessionHelper
from core.helpers.s3_naming_helper import S3NamingHelper 
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


# S3 Naming Helper

def test_validate_bucket_name():
    helper = S3NamingHelper()

    # must be between 3-63 chars
    response = helper.validate_bucket_name('ab')
    assert not response[0], 'allowed bucket name that was too short'

    response = helper.validate_bucket_name(
        ''.join([str(x) for x in range(0, 65)]))
    assert not response[0], 'allowed bucket name that was too long'

    # lower case chars, numbers, periods, dashes

    response = helper.validate_bucket_name('_$Bucket')
    assert not response[0], 'allowed bucket name with invalid chars'

    # cannot end with dash

    response = helper.validate_bucket_name('bucket-')
    assert not response[0], 'allowed bucket name with dash ending'

    # cannot consecutive periods
    response = helper.validate_bucket_name('bucket..')
    assert not response[0], 'allowed bucket name with double periods'

    # dashes next to periods
    response = helper.validate_bucket_name('bucket-.')
    assert not response[0], 'allowed bucket name with dash next to period'

    # char or number after period
    response = helper.validate_bucket_name('bucket.')
    assert not response[0], 'allowed bucket name without a letter or number after period'

    # char or number at start
    response = helper.validate_bucket_name('_bucket')
    assert not response[0], 'allowed bucket name without a letter or number to start'

    # valid
    response = helper.validate_bucket_name('bucket')
    assert response[0], f'failed to validate valid name - message {response[1]}'


def test_validate_part():
    helper = S3NamingHelper()
    response = helper.validate_part('this/is/invalid', allow_prefix=False)

    assert not response[0], f'allowed prefix when prefix was disallowed'

    response = helper.validate_part('')
    assert not response[0], f'allowed blank part'

    response = helper.validate_part('/abc/$$!badval/def')
    assert not response[0], f'allowed bad compound part'


def test_validate_s3_path():
    helper = S3NamingHelper()

    response = helper.validate_s3_path('abc/not/valid')
    assert not response[0], f'allowed s3 path without arn prefix'

    response = helper.validate_s3_path('s3://%%$Bucket_name/is/bad')
    assert not response[0], f'allowed bad bucket name'

    response = helper.validate_s3_path('s3://bucket/path/B#)$_ad/dataset')
    assert not response[0], f'allowed bad bucket prefix'

    response = helper.validate_s3_path('s3://bucket/path/all/good')
    assert response[0], f'disallowed good s3 path'


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
