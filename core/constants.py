import os
import yaml
from .helpers.project_root import ProjectRoot
from git import Repo

## IMPORTANT: config/core_project.yaml is in core's .gitignore, be sure to remove it before making
## any changes to constants

## DYNAMICS
# AWS_ACCOUNT default is set to PROD_AWS_ACCOUNT for prod and uat, DEV_AWS_ACCOUNT otherwise
# BATCH_JOB_QUEUE default is set to '<ENVIRONMENT>-core'
# ENV_BUCKET default is set to 'ichain-<ENVIRONMENT>' 

def reset_constants():
    ''' sets (or resets) constants based on hierarchy of 
        1) current envars that begin with ICHAIN_
        2) values defined in core_project.yml
    '''
    config_file = os.path.join(
        ProjectRoot().get_path(), 'config', 'core_project.yaml')
    with open(config_file) as _file:
        config = yaml.safe_load(_file)
        for k, v in config.items():
            globals()[k] = v

    # set constants from all envars starting with ICHAIN_. Override those set in the yaml file
    for key in os.environ.keys():
        if key[:7] == 'ICHAIN_':
            globals()[key.replace('ICHAIN_', '')] = os.environ[key]

    # set the branch name based on the current repo branch, and account for Jenkins weirdness with detached heads
    def get_branch_name():
        # if we already picked up branch name from ICHAIN_BRANCH_NAME, leave it
        if 'ICHAIN_BRANCH_NAME' in os.environ.keys():
            return os.environ["ICHAIN_BRANCH_NAME"]
        # if dev, we need to use the branch name or the os environment variable for jenkins
        elif globals()['ENVIRONMENT'] == 'dev':
            try:
                repo = Repo(ProjectRoot().get_path())
                return repo.active_branch.name

            # jenkins weirdness in dev
            except:
                return os.environ['BRANCH_NAME']
        # for prod and uat if they are hard-coded? for whatever reason, use the environment name
        else:
            return globals()['ENVIRONMENT']

    def get_env_bucket():
        if 'ICHAIN_ENV_BUCKET' in os.environ.keys():
            return os.environ['ICHAIN_ENV_BUCKET']
        else:
            return f"ichain-{globals()['ENVIRONMENT']}"

    def get_aws_account():
        if 'ICHAIN_AWS_ACCOUNT' in os.environ.keys():
            return os.environ['ICHAIN_AWS_ACCOUNT']
        elif globals()['ENVIRONMENT'] in ('prod', 'uat'):
            return globals()['PROD_AWS_ACCOUNT']
        else:
            return globals()['DEV_AWS_ACCOUNT']

    def get_batch_job_queue():
        if 'ICHAIN_BATCH_JOB_QUEUE' in os.environ.keys():
            return os.environ['ICHAIN_BATCH_JOB_QUEUE']
        else:
            return f"{globals()['ENVIRONMENT']}-core"

    def get_core_job_def_name():
        if 'ICHAIN_BATCH_JOB_DEFINITION_NAME' in os.environ.keys():
            return os.environ['ICHAIN_BATCH_JOB_DEFINITION_NAME']
        else:
            if ENVIRONMENT == 'dev':
                return f"core_{BRANCH_NAME}"
            elif ENVIRONMENT == 'uat':
                return "core_uat"
            elif ENVIRONMENT == 'prod':
                return "core_prod"    
            else:
                raise Exception(f"Can't create a core tag job definition name for environment {ENVIRONMENT}")

    # Dynamic (smart) Constants
    globals()['BRANCH_NAME'] = get_branch_name()
    globals()['ENV_BUCKET'] = get_env_bucket()
    globals()['AWS_ACCOUNT'] = get_aws_account()
    globals()['BATCH_JOB_QUEUE'] = get_batch_job_queue()
    globals()['BATCH_JOB_DEFINITION_NAME'] = get_core_job_def_name()

reset_constants()
