import click
from git import Repo
from core.helpers import notebook
from core.constants import DOCKER_REPO, AWS_ACCOUNT, DEV_AWS_ACCOUNT
from core.helpers.docker import CoreDocker
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
@click.argument('env', type=click.Choice(['local', 'dev']))
def publish(env):
    if env == 'local':
        AWS_ACCOUNT_ID = DEV_AWS_ACCOUNT
        repo = Repo('.')
        branch_name = repo.active_branch.name
        core_docker = CoreDocker()
        logger.info(f"Building image {DOCKER_REPO}:{branch_name} from current branch {branch_name}")
        full_tag = core_docker.build_image(f"{DOCKER_REPO}:{branch_name}")

        core_docker.register_image(branch_name, DOCKER_REPO, AWS_ACCOUNT_ID)
        ecr_tagged_image_name = core_docker.get_aws_repository(full_tag, AWS_ACCOUNT_ID)
        job_def_name = f"core_{branch_name}"
        logger.info(f"Registering AWS Batch job definition {job_def_name} that depends on ECR Image {ecr_tagged_image_name}.")
        core_docker.register_job_definition(job_def_name, ecr_tagged_image_name)
    if env == 'dev':
        AWS_ACCOUNT_ID = DEV_AWS_ACCOUNT
        repo = Repo('.')
        branch_name = repo.active_branch.name
        core_docker = CoreDocker()
        logger.info(f"Building image {DOCKER_REPO}:latest from current branch {branch_name}")
        full_tag = core_docker.build_image(f"{DOCKER_REPO}:latest")

        core_docker.register_image('latest', DOCKER_REPO, AWS_ACCOUNT_ID)
        ecr_tagged_image_name = core_docker.get_aws_repository(full_tag, AWS_ACCOUNT_ID)
        job_def_name = "core"
        logger.info(f"Registering AWS Batch job definition {job_def_name} that depends on ECR Image {ecr_tagged_image_name}.")
        core_docker.register_job_definition(job_def_name, ecr_tagged_image_name)


@cli.command()
@click.argument('env', type=click.Choice(['local']))
def tidy(env):
    if env == 'local':
        AWS_ACCOUNT_ID = DEV_AWS_ACCOUNT
        repo = Repo('.')
        branch_name = repo.active_branch.name
        full_tag = f'{DOCKER_REPO}:{branch_name}'
        job_def_name = f"core_{branch_name}"

        #Remove batch job definition
        core_docker = CoreDocker()
        logger.info(f"Deregistering all revisions of {job_def_name}")
        core_docker.deregister_job_definition_set(job_def_name)
        try:
            logger.info(f"Removing all revisions of {job_def_name} from account {AWS_ACCOUNT_ID}")
            core_docker.remove_ecr_image(branch_name, DOCKER_REPO, AWS_ACCOUNT_ID)
            logger.info(f"Removing local image {full_tag}")
            core_docker.remove_image(full_tag)
        except ImageNotFound:
            logger.warn(f"Nothing to remove. Image {full_tag} not found.")


@cli.command()
@click.argument('id', type=int)
@click.argument('input_contract', type=str)
@click.argument('output_contract', type=str)
def run(id, input_contract, output_contract):
    notebook_url = notebook.run_transform(id, input_contract, output_contract)
    logger.info(f"Running notebook see output at {notebook_url}")