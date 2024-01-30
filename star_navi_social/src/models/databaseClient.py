from asyncio import current_task
import asyncpg
from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import AsyncAdaptedQueuePool
from src.config import settings

Base = declarative_base()

engine = create_async_engine(
    settings.db_url(),
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
            user=settings.PG_USER, 
            database=settings.PG_DB_NAME, 
            password=settings.PG_PASSWORD,
            host=settings.PG_HOST,
            port=settings.PG_PORT
        )
    except asyncpg.exceptions.InvalidCatalogNameError:
        # Database does not exist, create it.
        sys_conn = await asyncpg.connect(
            database=default_db, 
            user=settings.PG_USER, 
            password=settings.PG_PASSWORD,
            host=settings.PG_HOST,
            port=settings.PG_PORT
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{settings.PG_DB_NAME}" OWNER "{settings.PG_USER}"'
        )
        await sys_conn.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# @asynccontextmanager
async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
