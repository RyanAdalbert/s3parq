import click
from core.helpers import notebook


@click.group()
def cli(): # pragma: no cover
    pass

# Adjusting locked env variable from local -> dev for proper run, until env vars are adjusted per DC-157
@cli.command()
@click.argument('id', type=int)
@click.option('--branch', default=None, type=str)
@click.option('--parent', default=None, type=str)
@click.option('--child', default=None, type=str)
@click.option('--state', default=None, type=str)
def run(id, branch, parent, child, state):
    notebook_url = notebook.run_transform(id, branch=branch, parent=parent, child=child, state=state)
    print("See your notebook output at:")
    print(notebook_url)