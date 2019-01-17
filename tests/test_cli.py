import pytest
import click
import os
from click.testing import CliRunner
from core import cli
from core.helpers.project_root import ProjectRoot

@pytest.fixture
def cleanup_migration_files():
    def cleanup(files):
        for f in files:
            os.remove(ProjectRoot().get_path() + os.path.sep + 'database' + os.path.sep + f)
    return cleanup

def test_cli_add():
    runner = CliRunner()
    result = runner.invoke(cli.add, ["1", "2"])
    assert result.exit_code == 0
    assert result.output == '3\n\n'

def test_generate_configuration_migration(cleanup_migration_files):
    runner = CliRunner()
    result = runner.invoke(cli.generate_configuration_migration)
    assert result.output.strip().isnumeric()
    assert result.exit_code == 0
    
    ## cleanup if run locally
    if __name__ == '__main__':
        cleanup_migration_files(result.output + '_up.sql')
        cleanup_migration_files(result.output + '_down.sql')
   
