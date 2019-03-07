from core.models import configuration
from core import secret, contract
from core.constants import ENVIRONMENT, CORE_VERSION
from core.helpers import notebook

import os
import tempfile
from core.logging import LoggerMixin
import pandas as pd
from os import path
from encodings.aliases import aliases
from datetime import datetime

class InitialIngestTransform(LoggerMixin):

    def __init__(self, input_contract, output_contract, transform):
        self.input_contract = input_contract
        self.output_contract = output_contract
        self.transform = transform

    def run(self):
        for config in self.transform.initial_ingest_configurations:
            self.validate_config(config)
            in_files = self.input_contract.list_files(config.input_file_prefix)
            run_timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')

            for file in files:
                filename = path.basename(file)
                with input_contract.download_raw_file(filename) as f:
                    df = self.ingest_file(f, filename)
                    self.output_contract.write_with_metadata(config.dataset, df, run_timestamp)

    def ingest_file(self, f, filename):
        input_s3_url = input_contract.get_s3_url(filename)
        df = pd.read_csv(f, dtype="str", encoding=config.encoding, sep=config.delimiter, skip_rows=config.skip_rows)
        df = self.set_initial_metadata(df, input_s3_url, run_timestamp)
        return df

    def validate_config(self, config):
        valid_encodings = set(aliases.keys+aliases.values)

        if config.encoding not in valid_encodings:
            invalid_encoding_message = f"initial_ingest_configuration {config.id} has invalid encoding: {config.encoding}"
            self.logger.critical(invalid_encoding_message)
            raise ValueError(invalid_encoding_message)
        if len(config.delimiter) < 1:
            invalid_delimiter_message = f"initial_ingest_configuration {config.id} has no delimiter"
            self.logger.critical(invalid_delimiter_message)
            raise ValueError(invalid_delimiter_message)

    def set_initial_metadata(self, df, s3_url, run_timestamp):
        df['__metadata_original_s3_url'] = s3_url
        df['__metadata_ingest_timestamp'] = run_timestamp
        return df

                
            # Get a list of all the files of interest
                # Get their metadata

            # Get the metadata of the target location


            # Check if the file meets

    # def csv_to_df(self, delimiter, skip_rows, encoding, filename_prefix, dataset):