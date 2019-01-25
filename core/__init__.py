__project__ = 'core'
__version__ = '0.0.1'

import os
import yaml
from .helpers.project_root import ProjectRoot

config_file = os.path.join(ProjectRoot().get_path(),'core_project.yaml')
with open(config_file) as _file:
    config = yaml.safe_load(_file)
    for k, v in config.items():
        globals()[k] = v
