from airflow.utils import  apply_defaults
from airflow.operators.bash_operator import BashOperator
from git import Repo
from collections import namedtuple
from core.contract import Contract
from core.helpers.project_root import ProjectRoot
from core.helpers.session_helper import SessionHelper
import core.models.configuration as config


class TransformOperator(BashOperator):

    @apply_defaults
    def __init__(self, transform_id:int, *args, **kwargs) -> None:
        """ Transformation operator for DAGs. 
                **kwargs are direct passed into super - BaseOperator from Airflow
                returns a valid task object for use in DAGs only
        """
        self.transform_id = transform_id
        task_id = self._generate_task_id()
        run_command = self._generate_run_command()

        super(TransformOperator, self).__init__(task_id=task_id, bash_command=run_command, *args, **kwargs)


    def _generate_run_command(self) -> str:
        """ Generates the run command to call corebot with
                This includes the subbed transform info
        """
        params = self._generate_contract_params()
        tranform_id = self.transform_id

        run_command = f'corebot run {tranform_id} --branch={params.branch} --parent={params.parent} --child={params.child} --state={params.state}'

        return run_command


    def _get_transform_info(self):
        """ Gets full queried info for the transform.
                Uses SessionHelper to grab it based on the transform ID
                TODO: Throw detailed exception if no transform exists
        """
        session = SessionHelper().session
        transform_config = config.Transformation
        transform = session.query(transform_config).filter(transform_config.id == self.transform_id).one()
        return transform


    def _generate_task_id(self) -> str:
        """ Creates full task_id for the transform task. 
                This is a unique string ID that can only correlate to this task.
                ID format = {pipeline_name}_{pipeline_state_type}_{transform_name}_{transform_id}
                    All set to lower case for matching up
        """
        transform = self._get_transform_info()
        p_name = transform.pipeline_state.pipeline.name
        p_stname = transform.pipeline_state.pipeline_state_type.name
        t_name = transform.transformation_template.name
        task_id = f"{p_name}_{p_stname}_{t_name}_{self.transform_id}".lower()
        return task_id


    def _generate_contract_params(self) -> [str]:
        """ Generates the params for contract creation
            This passes them over in string form, since contracts cant be directly passed that way
                allowing the receiving functions to quickly create without touching the configs schema
        """
        transform = self._get_transform_info()
        repo = Repo(ProjectRoot().get_path())

        branch = repo.active_branch.name.lower()
        parent = transform.pipeline_state.pipeline.brand.pharmaceutical_company.name.lower()
        child = transform.pipeline_state.pipeline.brand.name.lower()
        state = transform.pipeline_state.pipeline_state_type.name.lower()

        contract_tuple = namedtuple("params", ["branch","parent","child","state"])
        contract_params = contract_tuple(branch,parent,child,state)

        return contract_params
