import click
from core.helpers import notebook


@click.group()
def cli(): # pragma: no cover
    pass

# Adjusting locked env variable from local -> dev for proper run, until env vars are adjusted per DC-157
@cli.command()
@click.argument('env', type=click.Choice(['dev']))
@click.argument('id', type=int)
@click.argument('input_contract', type=str)
@click.argument('output_contract', type=str)
def run(env, id, input_contract, output_contract):
    notebook_url = notebook.run_transform(env, id, input_contract, output_contract)
    print("See your notebook output at:")
    print(notebook_url)