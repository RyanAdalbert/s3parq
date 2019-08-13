import click
from core.helpers import notebook
from core.constants import ENVIRONMENT, CORE_VERSION
from docker.errors import ImageNotFound
from core.logging import get_logger

logger = get_logger(__name__)

@click.group()
def cli(): # pragma: no cover
    pass

@cli.command()
@click.argument('id', type=int)
@click.argument('input_contract', type=str)
@click.argument('output_contract', type=str)
def run(id, input_contract, output_contract):
    notebook_url = notebook.run_transform(id, input_contract, output_contract)
    logger.info(f"Running notebook see output at {notebook_url}")