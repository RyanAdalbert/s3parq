import pytest
import boto3
from moto import mock_secretsmanager
from core.secret import Secret

@pytest.fixture
def setup_secretsmanager_mock():
    mock = mock_secretsmanager()
    mock.start()
    

@pytest.fixture
def seed_mock_secrets():
    ftp_secret_string = '{"username":"GOB_Bluth", "password":"S3@L_s@le", "host":"ftp://bluth.com", "port":"22", "mode":"active","method":"SFTP"}'
    mysql_secret_string = '{"username":"ic_db_user", "password":"uns3cur3", "host":"12345-host.aws.integrichain.net", "port":"3306", "database": "bluth", "rdbms":"mysql"}'
    psql_read_secret_string = '{"username":"ic_db_user2", "password":"uns3cur3", "host":"22222-host.aws.integrichain.net", "port":"5432", "database": "configuration_application", "rdbms":"postgres", "schema":"public", "role":"public"}'
    psql_write_secret_string = '{"username":"ic_db_user2", "password":"uns3cur3", "host":"22222-host.aws.integrichain.net", "port":"5432", "database": "configuration_application", "rdbms":"postgres", "schema":"public", "role":"configurator"}'

    mock_secret = boto3.client('secretsmanager', region_name = 'us-east-1')
    
    mock_secret.create_secret(  Name = 'all/FTP/bluth/read',
                                Description = 'FTP connection for bluth source data.',
                                SecretString = ftp_secret_string
                             ) 

    mock_secret.create_secret(  Name = 'prod/database/bluth/write',
                                Description = 'Intermediary publish table for bluth transformed data.',
                                SecretString = mysql_secret_string
                             ) 

    mock_secret.create_secret(  Name = 'all/database/configuration_application/read',
                                Description = 'Read connection for the production configuration database.',
                                SecretString = psql_read_secret_string
                             ) 

    mock_secret.create_secret(  Name = 'prod/database/configuration_application/write',
                                Description = 'Write connection for the production configuration database.',
                                SecretString = psql_write_secret_string
                             ) 


def test_get_secret_with_args():
    secret = Secret(common_name='bluth',
                    env='dev',
                    type_of='FTP'
                    )

    assert secret.name == 'all/FTP/bluth/read'
    assert secret.password == "S3@L_s@le"

def test_get_secret_with_string():
    secret = Secret(name='prod/database/bluth/write')
    assert secret.common_name == 'bluth'
    assert secret.password == 'uns3cur3'

def test_none_empty_vals():
    secret = Secret(common_name='bluth',
                    env='all',
                    type_of='FTP')

    assert secret.schema == None
