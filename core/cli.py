import click
from git import Repo
from core.helpers import docker, notebook
from core.constants import DOCKER_REPO, AWS_ACCOUNT 



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
@click.argument('env', type=click.Choice(['local']))
def publish(env):
    if env == 'local':
        AWS_ACCOUNT_ID = AWS_ACCOUNT
        repo = Repo('.')
        branch_name = repo.active_branch.name
        print("Hang tight building this image can take a while...")
        full_tag = docker.build_image(f"{DOCKER_REPO}:{branch_name}")

        docker.register_image(branch_name, DOCKER_REPO, AWS_ACCOUNT_ID)
        ecr_tagged_image_name = docker.get_aws_repository(full_tag, AWS_ACCOUNT_ID)
        job_def_name = f"core_{branch_name}"
        docker.register_job_definition(job_def_name, ecr_tagged_image_name)


@cli.command()
@click.argument('env', type=click.Choice(['local']))
def tidy(env):
    if env == 'local':
        AWS_ACCOUNT_ID = AWS_ACCOUNT
        repo = Repo('.')
        branch_name = repo.active_branch.name
        full_tag = f'{DOCKER_REPO}:{branch_name}'

        #Remove batch job definition
        job_def_name = f"core_{branch_name}"
        docker.deregister_job_definition_set(job_def_name)

        docker.remove_ecr_image(branch_name, DOCKER_REPO, AWS_ACCOUNT_ID)
        docker.remove_image(full_tag)

@cli.command()
@click.argument('env', type=click.Choice(['local']))
@click.argument('id', type=int)
@click.argument('input_contract', type=str)
@click.argument('output_contract', type=str)
def run(env, id, input_contract, output_contract):
    notebook_url = notebook.run_transform(env, id, input_contract, output_contract)
    print("See your notebook output at:")
    print(notebook_url)
