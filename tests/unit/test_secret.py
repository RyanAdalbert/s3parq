import os
import boto3
import pytest
from unittest.mock import patch
from core.secret import Secret
import moto


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")


@moto.mock_secretsmanager
def setup():
    secret_client = boto3.client('secretsmanager')
    ftp_secret_string = '{"user":"GOB_Bluth", "password":"S3@L_s@le", "host":"ftp://bluth.com", "port":"22", "mode":"active","method":"SFTP"}'
    mysql_secret_string = '{"user":"ic_db_user", "password":"uns3cur3", "host":"12345-host.aws.integrichain.net", "port":"3306", "database": "bluth", "rdbms":"mysql"}'
    psql_read_secret_string = '{"user":"ic_db_user2", "password":"uns3cur3", "host":"22222-host.aws.integrichain.net", "port":"5432", "database": "configuration_application", "rdbms":"postgres", "schema":"public", "role":"public"}'
    psql_write_secret_string = '{"user":"ic_db_user2", "password":"uns3cur3", "host":"22222-host.aws.integrichain.net", "port":"5432", "database": "configuration_application", "rdbms":"postgres", "schema":"public", "role":"configurator"}'
    secret_client.create_secret(Name='all/FTP/bluth/read',
                                Description='FTP connection for bluth source data.',
                                SecretString=ftp_secret_string
                                )

    secret_client.create_secret(Name='prod/database/bluth/write',
                                Description='Intermediary publish table for bluth transformed data.',
                                SecretString=mysql_secret_string
                                )

    secret_client.create_secret(Name='all/database/configuration_application/read',
                                Description='Read connection for the production configuration database.',
                                SecretString=psql_read_secret_string
                                )

    secret_client.create_secret(Name='prod/database/configuration_application/write',
                                Description='Write connection for the production configuration database.',
                                SecretString=psql_write_secret_string
                                )


@moto.mock_secretsmanager
def test_get_secret_with_args():
    setup()
    secret = Secret(name='bluth',
                    type_of='FTP',
                    mode='read'
                    )

    assert secret.identifier == 'dev/FTP/bluth/read'
    assert secret.password == "S3@L_s@le"


@moto.mock_secretsmanager
def test_get_secret_with_string():
    setup()
    secret = Secret(identifier='prod/database/bluth/write')
    assert secret.name == 'bluth'
    assert secret.password == 'uns3cur3'


@moto.mock_secretsmanager
@patch("core.secret.ENVIRONMENT", "prod")
def test_none_empty_vals():
    setup()
    secret = Secret(name='bluth',
                    type_of='database',
                    mode='write')

    assert secret.schema is None


@moto.mock_secretsmanager
@patch("core.secret.ENVIRONMENT", "Pretend-RSE")
def test_env_sub():
    setup()
    secret = Secret(name='configuration_application',
                    type_of='database', mode='read')
    assert secret.role == 'public'
