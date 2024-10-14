# ------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------

import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

from core.config import config

logger = logging.getLogger("uvicorn")
logging.getLogger("sqlalchemy.engine.Engine").handlers = logger.handlers

async_engine = create_async_engine(
    config.POSTGRES_URL,
    echo=True
)

async_sessionmaker = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


async def generate_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to yield an async SQLAlchemy ORM session.

    Yields:
        AsyncSession: An instance of an async SQLAlchemy ORM session.
    """
    async with async_sessionmaker() as async_session:
        yield async_session


async def test_connection():
    async with async_sessionmaker() as session:
        try:
            # Try to execute a simple query
            result = await session.execute(text("SELECT 1"))
            return result.scalar() == 1
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False