import os, yaml
from core.logging import LoggerSingleton

db_field = 'FORCE_POSTGRES'
yaml_loc = "config/core_project.yaml"

top = os.path.abspath(__file__)
top = os.path.dirname(os.path.dirname(os.path.dirname(top))) # redirects path to core root
yaml_path = os.path.join(top, yaml_loc)

logger = LoggerSingleton().logger

def postgres():
    with open(yaml_path) as f:
        doc = yaml.load(f)
    if doc[db_field] == False:
        doc[db_field] = True
        with open(yaml_path, 'w') as f:
            yaml.dump(doc, f, default_flow_style=False)
        logger.debug("Session helper set to use postgres.")
    else:
        logger.debug("Session helper is already set to use postgres.")

def cmock():
    with open(yaml_path) as f:
        doc = yaml.load(f)
    
    if doc[db_field] == True:
        doc[db_field] = False
        with open(yaml_path, 'w') as f:
            yaml.dump(doc, f, default_flow_style=False)
        logger.debug("Session helper set to use configuration mocker.")
    else:
        logger.debug("Session helper is already set to use configuration mocker.")

