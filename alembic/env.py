from logging.config import fileConfig
import asyncio
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import NullPool
from src.core.config import settings
from src.database.base import Base
from src.apps.esi.model import EsiUser, EsiToken

# Alembic Config object
config = context.config

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the database URL dynamically
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Include metadata from models
target_metadata = Base.metadata


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using AsyncEngine."""

    connectable: AsyncEngine = create_async_engine(
        settings.DATABASE_URL,
        poolclass=NullPool,
        future=True,
    )

    async with connectable.begin() as connection:
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn, target_metadata=target_metadata
            )
        )

        await connection.run_sync(lambda _: context.run_migrations())  # ✅ Fixed call


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())  # ✅ Properly run async migrations
