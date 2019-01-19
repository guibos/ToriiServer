from __future__ import with_statement

import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine.url import URL

from src.infractuture.configuration.configuration_repository import Configuration
from src.facade.database.service import combine_metadata
from src.facade.database.value_object import DatabaseURLValueObject

sys.path.append(os.getcwd())

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the configuration file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

target_metadata = combine_metadata()

# other values from the configuration, defined by the needs of env.py,
# can be acquired:
# my_important_option = configuration.get_main_option("my_important_option")
# ... etc.


def set_config() -> None:
    if not config.get_main_option("database_url.drivername"):
        url_config = Configuration().get_section(section='database')
        for key in url_config:
            if url_config[key]:  # Not None Values
                config.set_main_option(f'database_url.{key}', url_config[key])


def get_url() -> URL:
    return DatabaseURLValueObject(
        drivername=config.get_main_option('database_url.drivername'),
        username=config.get_main_option('database_url.username'),
        password=config.get_main_option('database_url.password'),
        host=config.get_main_option('database_url.host'),
        port=config.get_main_option('database_url.port'),
        database=config.get_main_option('database_url.database'),
        query=config.get_main_option('database_url.query'),
    ).get_url()


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(url=get_url(), target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    config_ini = config.get_section(config.config_ini_section)
    config_ini['sqlalchemy.url'] = get_url()
    connectable = engine_from_config(
        config_ini,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


set_config()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
