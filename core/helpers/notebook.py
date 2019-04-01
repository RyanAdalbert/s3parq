import papermill
from core.helpers import project_root
from core.constants import ENV_BUCKET
from core.helpers.session_helper import SessionHelper
from core.models import configuration

root = project_root.ProjectRoot().get_path()

def run_transform(transform_id:int) -> str:

    ## notebook name == transform_template.name
    t_configs = get_transform(transform_id)
    notebook = t_configs.transformation_template.name
    #Then run the notebook
    path = f"{root}/transforms/{notebook}.ipynb"
    papermill.execute_notebook(
        path,
        output_path       
        parameters = dict(id=transform_id),
        cwd=self.root
    )

    return output_url(output_s3_path)

# TODO: figure out how else we're going to separate the notebook 
def output_path(output_contract: str, transformation_name: str) -> str:
    s3_prefix = f"s3://{ENV_BUCKET}/notebooks"
    return f"{s3_prefix}/{output_contract}/{transformation_name}.ipynb"

def output_url(output_path: str) -> str:
    s3_prefix = "s3://{ENV_BUCKET}/notebooks"
    url_prefix = "http://notebook.integrichain.net/view"
    return output_path.replace(s3_prefix, url_prefix)

def get_transform(transform_id):
    session = SessionHelper().session
    transform_config = configuration.Transformation
    # Start querying the extract configs
    transform = session.query(transform_config).filter(transform_config.id == transform_id).one()
    return transform
