import moto
import pytest
from unittest.mock import patch
import click
from click.testing import CliRunner
from corebot import cli


# Mocking Notebook class - avoids re-testing complex logic and increasing brittleness
@patch('core.helpers.notebook.run_transform')
def test_corebot_run_notebook_transform(notebook_transform):
    runner = CliRunner()
    result = runner.invoke(cli.run, ("dev",1,"test_input_contract","test_output_contract"))
    assert notebook_transform.called_once_with("dev", 1, "test_input_contract","test_output_contract")
