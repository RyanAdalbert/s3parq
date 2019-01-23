import click
from git import Repo
from core.helpers import docker

DOCKER_REPO = 'ichain/core'

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
        AWS_ACCOUNT_ID = "687531504312"
        repo = Repo('.')
        branch_name = repo.active_branch.name
        full_tag = docker.build_image(f"{DOCKER_REPO}:{branch_name}")

        docker.register_image(branch_name, DOCKER_REPO, AWS_ACCOUNT_ID)

@cli.command()
@click.argument('env', type=click.Choice(['local']))
def tidy(env):
    if env == 'local':
        AWS_ACCOUNT_ID = "687531504312"
        repo = Repo('.')
        branch_name = repo.active_branch.name
        full_tag = f'{DOCKER_REPO}:{branch_name}'

        docker.remove_ecr_image(branch_name, DOCKER_REPO, AWS_ACCOUNT_ID)
        docker.remove_image(full_tag)

@cli.command()
@click.argument('env', type=click.Choice(['local']))
def run(env):
    docker.build_branch_image()
