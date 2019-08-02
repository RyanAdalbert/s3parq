from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from airflow.utils.decorators import apply_defaults
from airflow.contrib.operators.awsbatch_operator import AWSBatchOperator
from airflow.contrib.operators.ssh_operator import SSHOperator
from collections import namedtuple
from core.constants import BATCH_JOB_QUEUE, BRANCH_NAME, ENVIRONMENT, BATCH_JOB_DEFINITION_NAME
from core.contract import Contract
from core.helpers.project_root import ProjectRoot
from core.helpers.session_helper import SessionHelper
from airflow.contrib.hooks.ssh_hook import SSHHook
import core.models.configuration as config
from core.logging import get_logger

# inherit based on environment
InheritOperator = SSHOperator if ENVIRONMENT == 'dev' else AWSBatchOperator

class TransformOperator(InheritOperator):

    @apply_defaults
    def __init__(self, transform_id: int, **kwargs) -> None:
        """ Transformation operator for DAGs. 
                **kwargs are direct passed into super - PythonOperator from Airflow
                returns a valid task object for use in DAGs only
        """

        self.__logger = get_logger(
            ".".join([self.__module__, self.__class__.__name__]))

        self.transform_id = transform_id

        task_id = self._generate_task_id()

        params = self._generate_contract_params()
        
        job_def_name = BATCH_JOB_DEFINITION_NAME
        job_name = f'{params.parent}_{params.child}_{params.state}_{params.dataset}'
        job_queue = BATCH_JOB_QUEUE

        run_id = "{{ ti.xcom_pull(task_ids='RunEvent', key='run_id') }}"
        
        run_command = [
            'corebot',
            'run',
            f'{transform_id}',
            f'{run_id}'
        ]

        """ Run location control: this class inherits SSHOperator for dev, 
            AWSBatchOperator for prod  
        """
        if isinstance(self, SSHOperator):
            hook = SSHHook(remote_host='notebook',
                           port=22,
                           username='corebot_remote',
                           password='corebot_remote',
                           timeout=5000
                           )

            self.__logger.info(
                f"Running Corebot command `{run_command}` locally in notebook container...")
            super(TransformOperator, self).__init__(task_id=task_id,
                                                    ssh_hook=hook,
                                                    provide_context=True,
                                                    command=" ".join(run_command),  # SSH can only take a string here :(
                                                    **kwargs
                                                    )
            self.__logger.info(
                "Done. Corebot ran successfully in notebook container.")
        else:
            self.__logger.info(
                f"Running Corebot run command string: {run_command} in AWS Batch.")
            job_container_overrides = {
                'command': run_command
            }

            self.__logger.info(f"Executing AWSBatchOperator for {job_name}.")
            super(TransformOperator, self).__init__(task_id=task_id,
                                                    job_name=job_name,
                                                    job_definition=job_def_name,
                                                    job_queue=job_queue,
                                                    overrides=job_container_overrides,
                                                    **kwargs
                                                    )
            self.__logger.info(
                f"Done. AWSBatchOperator executed for {job_name}.")

    def _get_transform_info(self, session):
        """ Gets full queried info for the transform.
                Uses SessionHelper to grab it based on the transform ID
                TODO: Throw detailed exception if no transform exists
        """
        transform_config = config.Transformation
        # if the transform is missing for some reason, we want a clear error
        try:
            transform = session.query(transform_config).filter(
                transform_config.id == self.transform_id).one()
        except NoResultFound:
            raise SQLAlchemyError(
                f"Transform id {self.transform_id} was not found in the configuration database.")
        return transform

    def _generate_task_id(self) -> str:
        """ Creates full task_id for the transform task. 
                This is a unique string ID that can only correlate to this task.
                ID format = {pipeline_name}_{pipeline_state_type}_{transform_name}_{transform_id}
                    All set to lower case for matching up
        """
        session = SessionHelper().session
        transform = self._get_transform_info(session)
        p_name = transform.pipeline_state.pipeline.name
        p_stname = transform.pipeline_state.pipeline_state_type.name
        t_name = transform.transformation_template.name
        session.close()
        task_id = f"{p_name}_{p_stname}_{t_name}_{self.transform_id}".lower()
        self.__logger.debug(f"task_id: {task_id}")
        return task_id

    def _generate_contract_params(self) -> [str]:
        """ Generates the params for contract creation
            This passes them over in string form, since contracts cant be directly passed that way
                allowing the receiving functions to quickly create without touching the configs schema
        """
        session = SessionHelper().session
        transform = self._get_transform_info(session)
        parent = transform.pipeline_state.pipeline.brand.pharmaceutical_company.name.lower()
        child = transform.pipeline_state.pipeline.brand.name.lower()
        state = transform.pipeline_state.pipeline_state_type.name.lower()
        dataset = transform.transformation_template.name.lower()
        session.close()
        self.__logger.debug(
            f"Named contract params:: branch = {BRANCH_NAME}, parent = {parent}, child = {child}, state = {state}, dataset = {dataset}")
        contract_tuple = namedtuple(
            "params", ["branch", "parent", "child", "state", "dataset"])
        contract_params = contract_tuple(
            BRANCH_NAME, parent, child, state, dataset)

        return contract_params
