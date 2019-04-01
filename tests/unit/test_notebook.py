from mock import patch
import moto
import boto3
import pytest
import tempfile
from core.constants import ENV_BUCKET
import os
from io import TextIOWrapper
from core.helpers import notebook


@moto.mock_s3
class Test:
    def setup(self):
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=ENV_BUCKET)

    def test_output_path(self):
        self.setup()
        output_contract = "asdf/1234/merp/boomboom"
        output_path = notebook.output_path(
            output_contract)
        assert output_path == f"s3://{ENV_BUCKET}/notebooks/asdf/1234/merp/boomboom.ipynb"

    def test_output_url(self):
        self.setup()
        output_path = "s3://{ENV_BUCKET}/notebooks/asdf/1234/merp/shared.raw.extract.ipynb"
        output_url = notebook.output_url(output_path)
        assert output_url == "http://notebook.integrichain.net/view/asdf/1234/merp/shared.raw.extract.ipynb"

    @patch("core.helpers.notebook.papermill")
    def test_run_transform(self,mock_papermill):
        self.setup()
        s3 = boto3.resource('s3')
    
        bucket = ENV_BUCKET
        key = "notebooks/dev/important_business/raw/extract/shared.test.hello_world.ipynb"
        tid=2
        tbranch="test_branch"
        tstate="raw"
        tparent="merck"
        tchild="prilosec"
        notebook_url = notebook.run_transform(transform_id=tid)

        mock_papermill.execute_notebook.assert_called
        """
        with tempfile.TemporaryDirectory() as tmpdirname:
            test_file_location = os.path.join(tmpdirname, 'test.ipynb')
            s3.Bucket(bucket).download_file(key, test_file_location)

            # Make sure that it actually creates the output_notebook file
            # we could possibly create an actual test notebook with known
            # expected outputs if we like, but that might be overkill
            with open(test_file_location, 'r') as tmp_notebook:
                assert type(tmp_notebook) is TextIOWrapper
        """
