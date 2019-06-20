import os, yaml, sys
from core.logging import LoggerSingleton

db_field = 'FORCE_POSTGRES'
yaml_loc = "config/core_project.yaml"

top = os.path.abspath(__file__)
# redirects path to core root
top = os.path.dirname(os.path.dirname(os.path.dirname(top)))
yaml_path = os.path.join(top, yaml_loc)

logger = LoggerSingleton().logger

def is_postgres():
    with open(yaml_path) as f:
        doc = yaml.load(f)
    return doc[db_field]

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
        logger.debug(
            "Session helper is already set to use configuration mocker.")

if __name__ == "__main__": # requires arg -p or -m to specify postgres or config mocker
    if len(sys.argv) != 2 or sys.argv[1] not in ('-p', '-m'):
        logger.debug("Error: postgres_toggle must be called with exactly one argument, -p or -m.")
        sys.exit()
    if sys.argv[1] == '-p':
        postgres()
    else:
        cmock()
    sys.exit()
