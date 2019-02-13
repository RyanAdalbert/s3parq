from __future__ import with_statement

from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from core.models.configuration import Base
from core.secret import Secret
from core.constants import ENVIRONMENT
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def create_conn_string_from_secret():
    """ builds the appropriate db string based on ENV - specific secret.
        For dev uses the value in alembic.ini."""
    if ENVIRONMENT == "dev":
        return config.get_main_option("sqlalchemy.url")

    secret = Secret(env=ENVIRONMENT, 
                    name='configuration_application',
                    type_of='database',
                    mode='read'
                    )
    if secret.rdbms == "postgres":
        conn_string = f"postgresql://{secret.user}:{secret.password}@{host}/{database}"
    else:
        m = "Only postgres databases are supported for configuration_application at this time."
        logger.critical(m)
        raise NotImplementedError(m)
    return conn_string

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = create_conn_string_from_secret()    
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(create_conn_string_from_secret())

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
