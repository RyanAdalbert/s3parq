import click
from core.helpers import notebook


@click.group()
def cli(): # pragma: no cover
    pass

# Adjusting locked env variable from local -> dev for proper run, until env vars are adjusted per DC-157
@cli.command()
@click.argument('id', type=int)
@click.argument('run_id', type=int)
def run(id, run_id):
    notebook_url = notebook.run_transform(id, run_id)
    print("See your notebook output at:")
    print(notebook_url)
