import moto
import boto3
import pytest
import tempfile
import os
from io import TextIOWrapper
from core.helpers import notebook

@moto.mock_s3
class Test:
    def setup(self):
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket="ichain-dev-gluepoc")

    def test_output_path(self):
        self.setup()
        output_contract = "asdf/1234/merp"
        transformation_name = "shared.raw.extract"
        output_path = notebook.output_path(output_contract, transformation_name)
        assert output_path == "s3://ichain-dev-gluepoc/notebooks/asdf/1234/merp/shared.raw.extract.ipynb"

    def test_output_url(self):
        self.setup()
        output_path = "s3://ichain-dev-gluepoc/notebooks/asdf/1234/merp/shared.raw.extract.ipynb"
        output_url = notebook.output_url(output_path)
        assert output_url == "http://notebook.integrichain.net/view/asdf/1234/merp/shared.raw.extract.ipynb"

    def test_run_transform(self):
        self.setup()
        s3 = boto3.resource('s3')

        bucket = "ichain-dev-gluepoc"
        key = "notebooks/dev/important_business/raw/extract/shared.raw.extract.ipynb"
        notebook_url = notebook.run_transform("dev", 2, "dev/important_business/raw/ftp", "dev/important_business/raw/extract")

        with tempfile.TemporaryDirectory() as tmpdirname:
            test_file_location = os.path.join(tmpdirname, 'test.ipynb')
            s3.Bucket(bucket).download_file(key, test_file_location)

            # Make sure that it actually creates the output_notebook file
            # we could possibly create an actual test notebook with known
            # expected outputs if we like, but that might be overkill
            with open(test_file_location, 'r') as tmp_notebook:
                assert type(tmp_notebook) is TextIOWrapper