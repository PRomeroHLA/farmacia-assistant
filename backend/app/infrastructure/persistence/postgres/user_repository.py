"""Repositorio de usuarios sobre PostgreSQL (SQLAlchemy async)."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application.ports import UserRepository
from app.domain.entities import User
from app.infrastructure.persistence.models import UserModel


def _row_to_user(row: UserModel) -> User:
    """Mapea fila ORM a entidad de dominio (incluye password_hash para uso interno en login)."""
    return User(
        id=row.id,
        username=row.username,
        full_name=row.full_name,
        password_hash=row.password_hash,
    )


class PostgresUserRepository(UserRepository):
    """Implementación de UserRepository con PostgreSQL. Usa un sessionmaker async inyectado."""

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session_maker = session_maker

    async def get_by_username(self, username: str) -> User | None:
        async with self._session_maker() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.username == username).limit(1)
            )
            row = result.scalar_one_or_none()
            if row is None:
                return None
            return _row_to_user(row)

    async def get_by_id(self, id: str) -> User | None:
        async with self._session_maker() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.id == id).limit(1)
            )
            row = result.scalar_one_or_none()
            if row is None:
                return None
            return _row_to_user(row)

    async def add(self, user: User) -> None:
        if user.password_hash is None or user.password_hash == "":
            raise ValueError("password_hash es obligatorio al añadir usuario en Postgres")
        async with self._session_maker() as session:
            async with session.begin():
                model = UserModel(
                    id=user.id,
                    username=user.username,
                    full_name=user.full_name,
                    password_hash=user.password_hash,
                )
                session.add(model)
