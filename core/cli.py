import click
from git import Repo
from core.helpers import notebook
from core.constants import DOCKER_REPO, AWS_ACCOUNT, DEV_AWS_ACCOUNT
from core.helpers.docker import CoreDocker
from docker.errors import ImageNotFound
from core.logging import get_logger
import os

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


def get_image_tag(environment: str):
    if environment == 'local':
        repo = Repo('.')
        try:
            branch_name = repo.active_branch.name
        except:
            branch_name = os.environ['BRANCH_NAME']
        return f"{DOCKER_REPO}:{branch_name}"
    elif environment == 'uat':
        return f"{DOCKER_REPO}:uat"
    elif environment == 'prod':
        return f"{DOCKER_REPO}:prod"

def get_job_def_name(environment: str):
    if environment == 'local':
        repo = Repo('.')
        try:
            branch_name = repo.active_branch.name
        except:
            branch_name = os.environ['BRANCH_NAME']
        return f"core_{branch_name}"
    elif environment == 'uat':
        return "core_uat"
    elif environment == 'prod':
        return "core_prod"    

def get_aws_account(environment: str):
    if environment == 'local':
        return DEV_AWS_ACCOUNT
    elif environment == 'uat':
        return PROD_AWS_ACCOUNT
    elif environment == 'prod':
        return PROD_AWS_ACCOUNT

@cli.command()
@click.argument('env', type=click.Choice(['local', 'dev']))
def publish(env):
    core_docker = CoreDocker()
    tag = get_image_tag(env)
    job_def_name = get_job_def_name(env)
    aws_account_id = get_aws_account(env)
    aws_tag = core_docker.get_aws_tag(tag, aws_account_id)
    job_role_arn = f"arn:aws:iam::{aws_account_id}:role/ecs-tasks"

    logger.info(f"Building docker image {tag}")
    core_docker.build_image(tag)
    core_docker.register_image(tag, DOCKER_REPO, aws_account_id)

    logger.info(f"Registering AWS Batch job definition {job_def_name} that depnds on image {tag}")
    core_docker.register_job_definition(job_def_name, aws_tag, job_role_arn)


@cli.command()
@click.argument('env', type=click.Choice(['local']))
def tidy(env):
    core_docker = CoreDocker()
    aws_account_id = get_aws_account(env)
    tag = get_image_tag(env)
    job_def_name = get_job_def_name(env)

    logger.info(f"Deregistering all revisions of {job_def_name}")
    core_docker.deregister_job_definition_set(job_def_name)
    try:
        logger.info(f"Removing all revisions of {job_def_name} from account {aws_account_id}")
        core_docker.remove_ecr_image(tag, DOCKER_REPO, aws_account_id)
        logger.info(f"Removing local image {tag}")
        core_docker.remove_image(tag)
    except ImageNotFound:
        logger.warn(f"Nothing to remove. Image {tag} not found.")


@cli.command()
@click.argument('env', type=click.Choice(['local']))
@click.argument('id', type=int)
@click.argument('input_contract', type=str)
@click.argument('output_contract', type=str)
def run(env, id, input_contract, output_contract):
    notebook_url = notebook.run_transform(env, id, input_contract, output_contract)
    logger.info(f"Running notebook see output at {notebook_url}")