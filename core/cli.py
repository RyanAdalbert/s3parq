import click
from core.helpers import notebook
from core.helpers import docker as c_docker
from core.constants import ENVIRONMENT
from docker.errors import ImageNotFound
from core.logging import get_logger

logger = get_logger(__name__)

@click.group()
def cli(): # pragma: no cover
    pass

@cli.command()
@click.argument('a', type=int)
@click.argument('b', type=int)
def add(a, b):
    click.echo(print(a + b))
    return a + b


@cli.command()
def publish():
    core_docker = c_docker.CoreDocker()
    tag = c_docker.get_core_tag()
    job_def_name = c_docker.get_core_job_def_name()
    aws_account_id = c_docker.get_aws_account()
    aws_tag = c_docker.get_aws_tag(tag, aws_account_id)
    job_role_arn = f"arn:aws:iam::{aws_account_id}:role/ecs-tasks"

    logger.info(f"Building docker image {tag}")
    core_docker.build_image(tag)
    core_docker.register_image(tag, aws_account_id)

    logger.info(f"Registering AWS Batch job definition {job_def_name} that depends on image {tag}")
    core_docker.register_job_definition(job_def_name, aws_tag, job_role_arn)


# This command scares me a bit, might need to have better guards against
# deleting all uat / production images / jobs.
@cli.command()
def tidy():
    if ENVIRONMENT != "dev":
        logger.warn(f"Can't run tidy in {ENVIRONMENT}.")
        return None
    core_docker = c_docker.CoreDocker()
    aws_account_id = c_docker.get_aws_account()
    tag = c_docker.get_core_tag()
    job_def_name = c_docker.get_core_job_def_name()

    logger.info(f"Deregistering all revisions of {job_def_name}")
    core_docker.deregister_job_definition_set(job_def_name)
    try:
        logger.info(f"Removing all revisions of {job_def_name} from account {aws_account_id}")
        core_docker.remove_ecr_image(tag, aws_account_id)
        logger.info(f"Removing local image {tag}")
        core_docker.remove_image(tag)
    except ImageNotFound:
        logger.warn(f"Nothing to remove. Image {tag} not found.")


@cli.command()
@click.argument('id', type=int)
@click.argument('input_contract', type=str)
@click.argument('output_contract', type=str)
def run(id, input_contract, output_contract):
    notebook_url = notebook.run_transform(id, input_contract, output_contract)
    logger.info(f"Running notebook see output at {notebook_url}")