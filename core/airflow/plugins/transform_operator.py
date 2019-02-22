from airflow.utils import  apply_defaults
from airflow.contrib.operators.awsbatch_operator import AWSBatchOperator
from git import Repo
from collections import namedtuple
from core.constants import BATCH_JOB_QUEUE
from core.contract import Contract
from core.helpers.project_root import ProjectRoot
from core.helpers.session_helper import SessionHelper
from core.helpers.docker import get_core_job_def_name
import core.models.configuration as config


class TransformOperator(AWSBatchOperator):

    @apply_defaults
    def __init__(self, transform_id:int, *args, **kwargs) -> None:
        """ Transformation operator for DAGs. 
                **kwargs are direct passed into super - PythonOperator from Airflow
                returns a valid task object for use in DAGs only
        """
        self.transform_id = transform_id
        task_id = self._generate_task_id()

        params = self._generate_contract_params()
        
        job_def_name = get_core_job_def_name()
        job_name = f'{params.parent}_{params.child}_{params.state}'
        job_queue = BATCH_JOB_QUEUE

        run_command = [
            'corebot',
            'run',
            f'{transform_id}',
            f'--branch={params.branch}',
            f'--parent={params.parent}',
            f'--child={params.child}',
            f'--state={params.state}'
        ]
        job_container_overrides = {
            'command': run_command
        }

        super(TransformOperator, self).__init__(task_id=task_id, 
                                                job_name=job_name, 
                                                job_definition=job_def_name, 
                                                job_queue=job_queue,
                                                overrides=job_container_overrides,
                                                *args, 
                                                **kwargs
                                                )

# @apply_defaults
#     def __init__(self,  overrides, max_retries=4200,
#                  aws_conn_id=None, region_name=None, **kwargs):
#         super(AWSBatchOperator, self).__init__(**kwargs)

#         self.aws_conn_id = aws_conn_id
#         self.region_name = region_name
#         self.overrides = overrides
#         self.max_retries = max_retries

#         self.jobId = None
#         self.jobName = None

#         self.hook = self.get_hook()

    # def _generate_batch_command_args(self) -> str:
    #     """ Generates the batch command for the PythonOperator to call
    #             This includes the corebot command as a container override
    #             job_name should be - 'pharmaceutical company'_'brand'_'state'
    #     """
    #     params = self._generate_contract_params()
        
    #     job_def_name = get_core_job_def_name()
    #     job_name = f'{params.parent}_{params.child}_{params.state}'
    #     job_queue = BATCH_JOB_QUEUE

    #     tranform_id = self.transform_id
    #     run_command = f'corebot run {tranform_id} --branch={params.branch} --parent={params.parent} --child={params.child} --state={params.state}'
    #     job_container_overrides = {
    #         'command': [
    #             run_command,
    #         ]
    #     }

    #     batch_command_args = {
    #                             "job_name":job_name, 
    #                             "job_definition":job_def_name, 
    #                             "job_queue":job_queue, 
    #                             "container_overrides":job_container_overrides
    #     }

    #     return batch_command_args

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
