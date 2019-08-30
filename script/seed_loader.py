from core.helpers.session_helper import SessionHelper as SHelp
import sqlalchemy
from alembic.command import upgrade
from alembic.config import Config
import os
import logging


def load_run_sql(seeds_dir, seed_file):
    '''
    Runs a SQL file using the SQLAlchecmy Session Helper
    '''
    logging.info(f'Executing {seeds_dir}{seed_file}')
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
load_run_sql(seeds_dir, "truncate_tables.sql")
load_run_sql(seeds_dir, "2019.02.13__14.02.sql")
load_run_sql(seeds_dir, "2019.04.15__14.19.sql")
load_run_sql(seeds_dir, "2019.07.08__09.41.sql")
load_run_sql(seeds_dir, "2019.07.19__09.20.sql")
load_run_sql(seeds_dir, "2019.08.05__13.40.sql")
load_run_sql(seeds_dir, "dispense_ingest_column_mapping.sql")
load_run_sql(seeds_dir, "patient_status_standardize_dates_template.sql")
load_run_sql(seeds_dir, "patient_status_standardize_dates.sql")
load_run_sql(seeds_dir, "patient_status_ingest_standardize_numbers_template.sql")
load_run_sql(seeds_dir, "patient_status_ingest_standardize_numbers.sql")
load_run_sql(seeds_dir, "patient_status_fill_rate_template.sql")
load_run_sql(seeds_dir, "patient_status_fill_rate.sql")
load_run_sql(seeds_dir, "enrich_pending_too_long_template.sql")
load_run_sql(seeds_dir, "enrich_pending_too_long.sql")
load_run_sql(seeds_dir, "patient_status_master_patient_status_template.sql")
load_run_sql(seeds_dir, "patient_status_master_patient_status.sql")
load_run_sql(seeds_dir, "patient_status_master_patient_status_variables.sql")
load_run_sql(seeds_dir, "patient_status_master_patient_substatus_template.sql")
load_run_sql(seeds_dir, "patient_status_master_patient_substatus.sql")
load_run_sql(seeds_dir, "patient_status_master_patient_substatus_variables.sql")
load_run_sql(seeds_dir, "patient_status_enrich_patient_journey_hierarchy_template.sql")
load_run_sql(seeds_dir, "patient_status_enrich_patient_journey_hierarchy.sql")
load_run_sql(seeds_dir, "patient_status_enrich_patient_journey_hierarchy_variables.sql")
load_run_sql(seeds_dir, "patient_status_enrich_fill_null_long_pat_id.sql")
load_run_sql(seeds_dir, "patient_status_ingest_brand_derivation.sql")
load_run_sql(seeds_dir, "patient_status_enrich_fill_null_ref_date.sql")
load_run_sql(seeds_dir, "enrich_cancel_before_active.sql")
logging.info("Seed loading complete!")
