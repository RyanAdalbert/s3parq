import boto3
import json
from core.logging import LoggerMixin
from core.constants import ENVIRONMENT

class Secret(LoggerMixin):
    ''' Abstracts aws secretsmanager - values of the secret are callable attributes. ie:
            secret = Secret(name='hamburger', env='dev', type_of='database', mode='read')
            secret.password 
            ## hot_dog

            secret.host
            ##hamburger.sandwich.com
        NOTE: if force_env is not set, the secret class will look for an "all" environment secret and return it
        when the specified environment fails. ie if 'dev/FTP/hamburger/read' does not exist, but 'all/FTP/hamburger/read' does,
        the values will be silently substituted. 
    '''

    def __init__(self, name: str = None,  type_of: str = None, mode: str = None, identifier: str = None, force_env: bool = False) -> None:
        ''' get the secret from secrets manager based on args.
            ARGS:
                - name (str): this is the human-readable name, also middle part of the fully formed secret contract
                - type_of (str): one of FTP, database, s3
                - mode (str): one of read / write 
                - identifier (str): if defined this is the fully formed secret contract exactly as it is in secrets manager
                - force_env (bool): if True, do not sub the universal secret (ie "all") when the given env is not found
        '''
        self.client = boto3.client('secretsmanager')
        if identifier:
            self._parse_identifier(identifier)
            self.identifier = identifier
        else:
            self.name = name
            self.environment = ENVIRONMENT
            self.type_of = type_of
            self.mode = mode
            self.identifier = self._build_identifier(
                name=name, env=ENVIRONMENT, type_of=type_of, mode=mode)

        raw_secret = self._get_secret(self.identifier, force_env)

        self._parse_secret(json.loads(raw_secret['SecretString']))

    def _parse_identifier(self, identifier: str) -> None:
        try:
            identifier_parts = identifier.split('/')
            self.environment, self.type_of, self.name, self.mode = identifier_parts
        except:
            raise ValueError(f'{identifier} is not a valid secret identifier')

    def _build_identifier(self, env: str, type_of: str, name: str, mode: str) -> str:
        return f'{env}/{type_of}/{name}/{mode}'

    def _get_secret(self, identifier: str, force_env: bool) -> str:
        # first look to see if the explicit secret exists
        self.logger.debug(f"Secret idenditifier {identifier}.")
        try:
            raw_secret = self.client.get_secret_value(SecretId=identifier)
        except Exception as e:
            if not force_env:
                # look for a universal secret with the same signature
                try:
                    self.logger.debug(f"Secret identifier not found, trying 'all/'")
                    raw_secret = self.client.get_secret_value(
                        SecretId='all/' + ('/'.join(identifier.split('/')[1:])))
                except:
                    raise e
            else:
                raise e
        return raw_secret

    def _parse_secret(self, secret: dict) -> None:
        if self.type_of == 'FTP':
            for val in ('user', 'password', 'host', 'method'):
                self.__dict__[val] = secret.get(val, None)
            self.connection_mode = secret['mode']
            if secret.get('port', None) is not None:
                self.port = int(secret.get('port'))
            else:
                self.port = None

        elif self.type_of == 'database':
            for val in ('user', 'password', 'rdbms', 'schema', 'role', 'host', 'database'):
                self.__dict__[val] = secret.get(val, None)
                self.port = int(secret.get('port', None))
