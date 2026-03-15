from abc import ABC, abstractmethod

from app.domain.entities import User


class UserRepository(ABC):
    """Puerto para persistencia de usuarios (auth). Las implementaciones pueden ser InMemory o Postgres."""

    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        """Obtiene un usuario por nombre de usuario."""
        ...

    @abstractmethod
    def get_by_id(self, id: str) -> User | None:
        """Obtiene un usuario por id."""
        ...

    @abstractmethod
    def add(self, user: User) -> None:
        """Añade o actualiza un usuario."""
        ...
