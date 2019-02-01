import os
import yaml
from .helpers.project_root import ProjectRoot

config_file = os.path.join(ProjectRoot().get_path(),'core_project.yaml')
with open(config_file) as _file:
    config = yaml.safe_load(_file)
    for k, v in config.items():
        # check to see if there's an environment variable
        # of the same name, if so, use it instead of the
        # value perscribed in core_project.yaml
        globals()[k] = os.getenv(k, v)
