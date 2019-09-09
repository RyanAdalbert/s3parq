from core.helpers.session_helper import SessionHelper as SHelp
from core.constants import ENVIRONMENT
import sqlalchemy
from alembic.command import upgrade
from alembic.config import Config
from glob import glob
import os
import logging

def load_run_sql(seeds_dir, seed_file):
    '''
    Runs a SQL file using the SQLAlchecmy Session Helper
    '''
    logging.info(f'Executing {seeds_dir}/{seed_file}')
    filepath = os.path.join(seeds_dir, seed_file)
    file = open(filepath)
    helper = SHelp()
    session = helper.session
    escaped_sql = sqlalchemy.text(file.read())
    session.execute(escaped_sql)
    session.close()
    logging.info(f'\tFinished')

seeds_dir = os.path.dirname('/host/core/seeds/')

logging.info("Starting seed loading...")
if ENVIRONMENT.lower() != "dev":
    load_run_sql(seeds_dir, "truncate_tables.sql")
load_run_sql(seeds_dir, "pharmaceuticals_and_brands.sql")
load_run_sql(seeds_dir, "statetypes_types_and_segments.sql")
load_run_sql(seeds_dir, "pipelines_and_pipelinestates.sql")
load_run_sql(seeds_dir, "administrators.sql")
load_run_sql(seeds_dir, "raw_extract_from_ftp.sql")
load_run_sql(seeds_dir, "initial_ingest.sql")
load_run_sql(seeds_dir, "dispense_ingest_column_mapping.sql")
load_run_sql(seeds_dir, "master_column_mocker.sql")

# List of all filenames in /seeds beginning with patient_status
patient_status_seeds = glob(os.path.join(seeds_dir, 'patient_status*'))
patient_status_seeds = list(map(os.path.basename, patient_status_seeds))

# patient_status_seeds.remove("filename.sql") to not load undesired patient_status seeds
patient_status_seeds.remove("patient_status_master_patient_secondary_benefit_type.sql")
for seed in patient_status_seeds:
    load_run_sql(seeds_dir, seed)

logging.info("Seed loading complete!")
