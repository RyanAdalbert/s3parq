from core.models import configuration
from core import secret, contract
from core.constants import ENVIRONMENT
from core.helpers import notebook

import os
import tempfile
from core.logging import LoggerMixin
import pandas as pd

def from_transform_id(id):
    t = notebook.get_transform(id)
    return InitialIngestTransform(
        id=t.id,
        configurations=t.initial_ingest_configurations,
        delimiter
    )


def list_objects(bucket: str, prefix: str) -> List[str]:
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket)
        objects = [obj.key for obj in bucket.objects.filter(Prefix=prefix)]

        return objects
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            raise FileNotFoundError("s3 object not found: %s" % prefix)
        else:
            raise

class InitialIngestTransform(LoggerMixin):

    def __init__(self, input_contract, output_contract, transform):
        self.input_contract = input_contract
        self.output_contract = output_contract
        self.transform = transform

    def run(self):
        input_path = self.input_contract.get_s3_path()

        for config in self.transform.initial_ingest_configurations:
            # Get a list of all the files of interest
                # Get their metadata

            # Get the metadata of the target location

            # Process 

            # Check if the file meets

    def csv_to_df(self, delimiter, skip_rows, encoding, filename_prefix, dataset):


    def