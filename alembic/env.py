import os
import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.models.user_model import Base
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env.test") or load_dotenv()

# Alembic config
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata
target_metadata = Base.metadata

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

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode with async support."""
    engine = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=None,
    )

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: context.configure(
            connection=sync_conn,
            target_metadata=target_metadata
        ))
        await conn.run_sync(lambda _: context.run_migrations())

    await engine.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
