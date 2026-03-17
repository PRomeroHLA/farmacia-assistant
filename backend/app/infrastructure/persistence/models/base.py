"""Base declarativa para modelos SQLAlchemy (async).

Usamos SQLAlchemy 2.x con AsyncAttrs + DeclarativeBase para habilitar
operaciones async en instancias ORM cuando sea necesario.
"""

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    """Base declarativa para todos los modelos ORM."""

    pass

