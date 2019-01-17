import click
from core.helpers import git, docker

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
        tag = docker.build_branch_image()
        

@cli.command()
@click.argument('env', type=click.Choice(['local']))
def run(env):
    docker.build_branch_image()