import click
from core.helpers.project_root import ProjectRoot
import subprocess
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
def generate_configuration_migration():
    ''' This generates an empty migration named with the current commit hash.
        It is far from a perfect way of aligning migrations with ORM code, but it's a spike in the ground. 
    '''
    path = ProjectRoot().get_path()
    git_hash = subprocess.check_output(['git','rev-parse','HEAD']).strip().decode()
    for suffix in ('up','down'):
        filepath = path + os.path.sep + 'database' + os.path.sep + git_hash + '_' + suffix + '.sql'
        open(filepath, "w").close()
    click.echo(git_hash)
    return git_hash
