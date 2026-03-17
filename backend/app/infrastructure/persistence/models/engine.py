"""Creación del engine y sessionmaker para SQLAlchemy async (PostgreSQL/asyncpg)."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def get_async_engine(database_url: str) -> AsyncEngine:
    """Crea y devuelve un AsyncEngine a partir de DATABASE_URL.

    Ejemplo: postgresql+asyncpg://user:password@localhost:5432/farmacia_db
    """
    return create_async_engine(database_url, future=True, pool_pre_ping=True)


def get_async_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Crea un sessionmaker para AsyncSession (SQLAlchemy 2.x)."""
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def async_session_scope(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    """Helper opcional: contexto async con commit/rollback automático."""
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

