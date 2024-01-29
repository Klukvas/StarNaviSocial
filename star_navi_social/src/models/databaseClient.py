from asyncio import current_task
import asyncpg
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.orm import declarative_base
from src.env import Env
from contextlib import asynccontextmanager

Base = declarative_base()

env = Env()

engine = create_async_engine(
    env.db_url,
    future=True,
    poolclass=AsyncAdaptedQueuePool,
    pool_reset_on_return=False,
    echo=True,
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

session = async_scoped_session(async_session_maker, scopefunc=current_task)


async def create_database_if_not_exist(default_db: str = "postgres") -> None:
    try:
        await asyncpg.connect(
            user=env.pg_user, database=env.pg_db_name, password=env.pg_password
        )
    except asyncpg.exceptions.InvalidCatalogNameError:
        # Database does not exist, create it.
        sys_conn = await asyncpg.connect(
            database=default_db, user=env.pg_user, password=env.pg_password
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{env.pg_db_name}" OWNER "{env.pg_user}"'
        )
        await sys_conn.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# @asynccontextmanager
async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
