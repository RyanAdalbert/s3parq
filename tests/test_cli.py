import pytest
import click
from click.testing import CliRunner
from core import cli


def test_cli_add():
    runner = CliRunner()
    result = runner.invoke(cli.add, ["1", "2"])
    assert result.exit_code == 0
    assert result.output == '3\n\n'

def test_generate_migration():
    runner = CliRunner()
    result = runner.invoke(cli.generate_migration)
    assert result.exit_code == 0
   
