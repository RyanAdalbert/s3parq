
import boto3
import moto 
import pytest
import os
from core.secret import Secret
import json

@moto.mock_secretsmanager
class Test:
    def setup(self):
        #self.save_env = dict()
        #self.AWS_VARS = ('AWS_ACCESS_KEY_ID','AWS_SECRET_ACCESS_KEY')
        #for var in self.AWS_VARS:
        #    self.save_env[var] = os.getenv(var)
        #    os.environ[var] = 'fake'
        
        secret_client = boto3.client('secretsmanager')
        ftp_secret_string = '{"user":"GOB_Bluth", "password":"S3@L_s@le", "host":"ftp://bluth.com", "port":"22", "mode":"active","method":"SFTP"}'
        mysql_secret_string = '{"user":"ic_db_user", "password":"uns3cur3", "host":"12345-host.aws.integrichain.net", "port":"3306", "database": "bluth", "rdbms":"mysql"}'
        psql_read_secret_string = '{"user":"ic_db_user2", "password":"uns3cur3", "host":"22222-host.aws.integrichain.net", "port":"5432", "database": "configuration_application", "rdbms":"postgres", "schema":"public", "role":"public"}'
        psql_write_secret_string = '{"user":"ic_db_user2", "password":"uns3cur3", "host":"22222-host.aws.integrichain.net", "port":"5432", "database": "configuration_application", "rdbms":"postgres", "schema":"public", "role":"configurator"}'
        secret_client.create_secret(  Name = 'all/FTP/bluth/read',
                                    Description = 'FTP connection for bluth source data.',
                                    SecretString = ftp_secret_string
                                 ) 

        secret_client.create_secret(  Name = 'prod/database/bluth/write',
                                    Description = 'Intermediary publish table for bluth transformed data.',
                                    SecretString = mysql_secret_string
                                 ) 

        secret_client.create_secret(  Name = 'all/database/configuration_application/read',
                                    Description = 'Read connection for the production configuration database.',
                                    SecretString = psql_read_secret_string
                                 ) 

        secret_client.create_secret(  Name = 'prod/database/configuration_application/write',
                                    Description = 'Write connection for the production configuration database.',
                                    SecretString = psql_write_secret_string
                                 ) 

    def teardown(self):
        for var in self.AWS_VARS:
            os.environ[var] = self.save_env[var]

    def test_get_secret_with_args(self):        
        self.setup()
        secret = Secret(name='bluth',
                        env='all',
                        type_of='FTP',
                        mode='read'
                        )

        assert secret.identifier == 'all/FTP/bluth/read'
        assert secret.password == "S3@L_s@le"

    def test_get_secret_with_string(self):
        self.setup()
        secret = Secret(identifier='prod/database/bluth/write')
        assert secret.name == 'bluth'
        assert secret.password == 'uns3cur3'

    def test_none_empty_vals(self):
        self.setup()
        secret = Secret(name='bluth',
                        env='prod',
                        type_of='database',
                        mode='write')

        assert secret.schema == None

    def test_env_sub(self):
        self.setup()
        secret = Secret(name='configuration_application', env='dev', type_of='database', mode='read')
        assert secret.role == 'public'
