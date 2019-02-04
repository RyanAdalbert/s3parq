import pytest
import click
from click.testing import CliRunner
from core import cli
import moto
'''
def test_cli_add():
    runner = CliRunner()
    result = runner.invoke(cli.add, ["1", "2"])
    assert result.exit_code == 0
    assert result.output == '3\n\n'
'''
def test_thing():
    assert True == True
