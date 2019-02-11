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


def get_image_tage(environment: str):
    if environment == 'local':
        repo = Repo('.')
        try:
            branch_name = repo.active_branch.name
        except:
            branch_name = os.environ['BRANCH_NAME']
        return f"{DOCKER_REPO}:{branch_name}:latest"
    elif environment == 'uat':
        return f"{DOCKER_REPO}:uat:latest"
    elif environment == 'prod':
        return f"{DOCKER_REPO}:prod:latest"

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
    tag = get_image_tage(env)
    job_def_name = get_job_def_name(env)
    aws_account_id = get_aws_account(env)
    aws_tag = core_docker.get_aws_tag(tag, aws_account_id)
    job_role_arn = f"arn:aws:iam::{aws_account_id}:role/ecs-tasks"

    logger.info(f"Building docker image {tag}")
    core_docker.build_image(tag)
    core_docker.register_image(tag, DOCKER_REPO, aws_account_id)

    logger.info(f"Registering AWS Batch job definition {job_def_name} that depnds on image {tag}")
    core_docker.register_job_definition(job_def_name, aws_tag, job_role_arn)



    # if env == 'local':
    #     AWS_ACCOUNT_ID = DEV_AWS_ACCOUNT
    #     repo = Repo('.')

    #     # Jenkins doesn't have an active branch name via git as it
    #     # checks things out via commit hash, so fall back to the
    #     # envirnment variable that Jenkins uses in that case.
    #     try:
    #         branch_name = repo.active_branch.name
    #     except:
    #         branch_name = os.environ['BRANCH_NAME']
    #     core_docker = CoreDocker()
    #     logger.info(f"Building image {DOCKER_REPO}:{branch_name} from current branch {branch_name}")
    #     full_tag = core_docker.build_image(f"{DOCKER_REPO}:{branch_name}")

    #     core_docker.register_image(branch_name, DOCKER_REPO, AWS_ACCOUNT_ID)
    #     ecr_tagged_image_name = core_docker.get_aws_repository(full_tag, AWS_ACCOUNT_ID)
    #     job_def_name = f"core_{branch_name}"
    #     logger.info(f"Registering AWS Batch job definition {job_def_name} that depends on ECR Image {ecr_tagged_image_name}.")
    #     core_docker.register_job_definition(job_def_name, ecr_tagged_image_name)
    # if env == 'dev':
    #     AWS_ACCOUNT_ID = DEV_AWS_ACCOUNT
    #     repo = Repo('.')
    #     branch_name = repo.active_branch.name
    #     core_docker = CoreDocker()
    #     logger.info(f"Building image {DOCKER_REPO}:latest from current branch {branch_name}")
    #     full_tag = core_docker.build_image(f"{DOCKER_REPO}:latest")

    #     core_docker.register_image('latest', DOCKER_REPO, AWS_ACCOUNT_ID)
    #     ecr_tagged_image_name = core_docker.get_aws_repository(full_tag, AWS_ACCOUNT_ID)
    #     job_def_name = "core"
    #     logger.info(f"Registering AWS Batch job definition {job_def_name} that depends on ECR Image {ecr_tagged_image_name}.")
    #     core_docker.register_job_definition(job_def_name, ecr_tagged_image_name)


@cli.command()
@click.argument('env', type=click.Choice(['local']))
def tidy(env):
    core_docker = CoreDocker()
    aws_account_id = get_aws_account(env)
    tag = get_image_tage(env)
    job_def_name = get_job_def_name(env)

    if env == 'local':
        #Remove batch job definition
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