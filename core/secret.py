import boto3



class Secret:
    
    def __init__(self, name: str = None, env: str = None, type_of: str = None, identifier: str = None, force_env: bool = False) -> None:
        ''' get the secret from secrets manager based on args.
            ARGS:
                - name (str): this is the human-readable name, also middle part of the fully formed secret contract
                - env (str): one of dev, prod, uat, all
                - type_of (str): one of FTP, database, s3
                - identifier (str): if defined this is the fully formed secret contract exactly as it is in secrets manager
                - force_env (bool): if True, do not sub the universal secret (ie "all") when the given env is not found
        ''' 
        self.client = boto3.client('secretsmanager','us-east-1')    
        if identifier:
            raw_secret = self._get_secret(identifier, force_env)
        elif name:
            raw_secret = self._get_secret(f'{env}/{type_of}/{name}/{mode}', force_env)
        else:
            raise ValueError('Secret requires either a name or identifier argument')
        
        
    

        
    def _get_secret(self, identifier: str) -> str:
        # first look to see if the explicit secret exists
        try:
            raw_secret = self.client.get_secret_value(identifier)
        except Exception, e:
            if not force_env:
                # look for a universal secret with the same signature
                try:
                    raw_secret = self.client.get_secret_value('all' + ('/'.join(identifier.split('/')[1:])))
                except:
                    raise e
            else:
                raise e 
        return raw_secret
            
       
       
