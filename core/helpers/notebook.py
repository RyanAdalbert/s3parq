import papermill as pm
from core.helpers import project_root
from core.constants import ENV_BUCKET
from core.helpers import configuration_mocker
from core.models import configuration
from core import contract

root = project_root.ProjectRoot()

def run_transform(id: int, state: str, branch: str, parent: str, child: str, name: str ="shared.raw.extract") -> str:
    # First you would look up the ID and get the name of the transform so you
    # know what notebook to run. Once the core transform code has been finalized and
    # you can reach out to a db to pull the name this hard-coding will be replaced.

    #Then run the notebook
    output_kontract = get_contract(state=state,branch=branch,parent=parent,child=child)
    output_contract = output_kontract.get_key()
    output_s3_path = output_path(output_contract, name)
    path = f"{root.get_path()}/transforms/{name.replace('.', '/')}.ipynb"
    pm.execute_notebook(
       path,
       output_s3_path,
       parameters = dict(id=id, branch=branch, parent=parent, child=child, state=state),
       cwd=root.get_path()
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

def get_input_contract(output_contract: contract.Contract, state, branch, parent, child) -> contract.Contract:
    if (output_contract.get_previous_state()==None):
        input_contract = None
    else:
        input_contract = get_contract(branch=branch,
                                    parent=parent,
                                    child=child,
                                    state=output_contract.get_previous_state())

    return input_contract

def get_contract(state, branch, parent, child):
    kontract = contract.Contract(state=state,
                                 branch=branch,
                                 parent=parent,
                                 child=child
                                 )
    return kontract

def get_transform(transform_id):
    config_mock = configuration_mocker.ConfigurationMocker()
    config_mock.generate_mocks()

    session = config_mock.get_session()

    ec = configuration.ExtractConfiguration
    t = configuration.Transformation

    # Start querying the extract configs
    transform = session.query(t).filter(t.id == transform_id).one()
    return transform
