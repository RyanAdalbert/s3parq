import boto3



class Secret:
    
    def __init__(self, common_name: str = None, env: str = None, type_of: str = None, name: str = None) -> None:
        ''' get the secret from secrets manager based on args.
            ARGS:
                - common_name (str): this is the human-readable name, also middle part of the fully formed secret contract
                - env (str): one of dev, prod, uat, all
                - type_of (str): one of FTP, database, s3
                - name (str): if defined this is the fully formed secret contract exactly as it is in secrets manager
        ''' 
        if not (common_name or name):
            raise ValueError('Secret requires either a name or common_name argument')
            
        
