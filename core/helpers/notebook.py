import papermill as pm
from core.helpers import project_root

root = project_root.ProjectRoot()

def run_transform(env: str, id: int, input_contract: str, output_contract: str) -> str:
    # First you would look up the ID and get the name of the transform so you
    # know what notebook to run. Once the core transform code has been finalized and
    # you can reach out to a db to pull the name this hard-coding will be replaced.
    name = "shared.raw.extract"

    #Then run the notebook
    output_s3_path = output_path(output_contract, name)
    path = f"{root.path}/transforms/{name.replace('.', '/')}.ipynb"
    pm.execute_notebook(
       path,
       output_s3_path,
       parameters = dict(id=id, input_contract=input_contract, output_contract=output_contract, env=env)
    )

    return output_url(output_s3_path)

# TODO: figure out how else we're going to separate the notebook 
def output_path(output_contract: str, transformation_name: str) -> str:
    s3_prefix = "s3://ichain-dev-gluepoc/notebooks"
    return f"{s3_prefix}/{output_contract}/{transformation_name}.ipynb"

def output_url(output_path: str) -> str:
    s3_prefix = "s3://ichain-dev-gluepoc/notebooks"
    url_prefix = "http://notebook.integrichain.net/view"
    return output_path.replace(s3_prefix, url_prefix)