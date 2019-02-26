import os
import yaml
from .helpers.project_root import ProjectRoot
from git import Repo

def reset_constants():
    ''' sets (or resets) constants based on hierarchy of 
        1) current envars that begin with ICHAIN_
        2) values defined in core_project.yml
    '''
    config_file = os.path.join(ProjectRoot().get_path(),'config','core_project.yaml')
    with open(config_file) as _file:
        config = yaml.safe_load(_file)
        for k, v in config.items():
            globals()[k] = v

    ## set constants from all envars starting with ICHAIN_. Override those set in the yaml file
    for key in os.environ.keys():
        if key[:7] == 'ICHAIN_':
            globals()[key.replace('ICHAIN_','')] = os.environ[key]
    
    ## set the branch name based on the current repo branch, and account for Jenkins weirdness with detached heads
    def get_branch_name():
        ## if we already picked up branch name from ICHAIN_BRANCH_NAME, leave it
        if 'ICHAIN_BRANCH_NAME' in os.environ.keys():
            return globals()['BRANCH_NAME']
        ## if dev, we need to use the branch name or the os environment variable for jenkins
        elif globals()['ENVIRONMENT'] == 'dev':
            try:
                repo = Repo(ProjectRoot().get_path())
                return repo.active_branch.name

            ## jenkins weirdness in dev
            except:
                return os.environ['BRANCH_NAME']
        ## for prod and uat use the environment name 
        else:
            return globals()['ENVIRONMENT']

    globals()['BRANCH_NAME'] = get_branch_name()

reset_constants()
