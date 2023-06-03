from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from app.config.config import db_url_alembic
from app.database.models.base import Base
from app.database.models.buisiness_entities import *
from alembic import operations


config = context.config
config.set_main_option('sqlalchemy.url', db_url_alembic)

fileConfig(config.config_file_name)

"""
Load models metadata. We should define schema in this class firstly, 
or set schema implicit with `__table_args__ = {'schema' : 'test'}` in model class
"""
target_metadata = Base.metadata

# Штука для генерации схем постгреса
def process_revision_directives(context, revision, directives):
    """Modify the MigrationScript directives to create schemata as required.
    """
    script = directives[0]
    for schema in frozenset(i.schema for i in target_metadata.tables.values()):
        script.upgrade_ops.ops.insert(
            0, operations.ops.ExecuteSQLOp(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
        script.downgrade_ops.ops.append(
            operations.ops.ExecuteSQLOp(f"DROP SCHEMA IF EXISTS {schema} RESTRICT"))




def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        process_revision_directives=process_revision_directives,
        target_metadata=target_metadata,
        literal_binds=True,
        url=url)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        """
        Configure migration context
        1. Pass our models metadata
        2. Set schema for alembic_version table
        3. Load all available schemas
        """
        context.configure(
            process_revision_directives=process_revision_directives,
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=target_metadata.schema,
            include_schemas=True
        )

        with context.begin_transaction():
            """
            By default search_path is setted to "$user",public 
            that why alembic can't create foreign keys correctly
            """
            context.execute('SET search_path TO public')
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()