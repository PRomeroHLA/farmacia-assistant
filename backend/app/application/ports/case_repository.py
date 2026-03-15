from abc import ABC, abstractmethod

from app.domain.entities import StructuredCase


class CaseRepository(ABC):
    """Puerto para persistencia de casos clínicos. Las implementaciones pueden ser InMemory o Postgres."""

    @abstractmethod
    def save(self, case: StructuredCase) -> str:
        """Guarda un caso y devuelve su id."""
        ...

    @abstractmethod
    def get_by_id(self, id: str) -> StructuredCase | None:
        """Obtiene un caso por id."""
        ...
