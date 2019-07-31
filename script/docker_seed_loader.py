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


def run_alembic_migrations():
    migrations_dir = os.path.dirname('/host/core/core/database/')
    config_file = os.path.join(migrations_dir, "alembic.ini")
    config = Config(file_=config_file)
    config.set_main_option("script_location", migrations_dir)
    upgrade(config, "head")

seeds_dir = os.path.dirname('/host/core/seeds/')

logging.info("Starting seed loading...")
run_alembic_migrations()
load_run_sql(seeds_dir, "2019.02.13__14.02.sql")
load_run_sql(seeds_dir, "2019.04.15__14.19.sql")
load_run_sql(seeds_dir, "2019.07.08__09.41.sql")
logging.info("Seed loading complete!")