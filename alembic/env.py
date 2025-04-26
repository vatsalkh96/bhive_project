from logging.config import fileConfig
from sqlalchemy import pool
# from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import create_engine
from alembic import context
import asyncio

from config import settings
from app.db.base import Base
from app import models  # makes sure models are imported and registered

# Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# Override DB URL from our settings
config.set_main_option("sqlalchemy.url", settings.sync_database_url)

# Target metadata
target_metadata = Base.metadata
connectable = create_engine(settings.sync_database_url)


def run_migrations_offline():
    context.configure(
        url=settings.sync_database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
