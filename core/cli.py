import click
from core.helpers.project_root import ProjectRoot
import time
import os
 
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
def generate_migration():
    ''' INTENT: creates paired 'up' and 'down' sql migration files
        RETURNS: None
    '''
    path = ProjectRoot().get_path()
    ts = str(time.time_ns())
    for suffix in ('up','down'):
        filepath = path + os.path.sep + 'database' + os.path.sep + ts + '_' + suffix + '.sql'
        open(filepath, "w").close()
    click.echo(f'created migration {ts}')

