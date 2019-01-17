import click
from git import Repo
from core.helpers import docker

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
        full_tag = docker.build_image(branch_name)
        docker.register_image(full_tag, AWS_ACCOUNT_ID)

@cli.command()
@click.argument('env', type=click.Choice(['local']))
def tidy(env):
    if env == 'local':
        repo = Repo('.')
        branch_name = repo.active_branch.name
        docker.remove_image(branch_name)

@cli.command()
@click.argument('env', type=click.Choice(['local']))
def run(env):
    docker.build_branch_image()