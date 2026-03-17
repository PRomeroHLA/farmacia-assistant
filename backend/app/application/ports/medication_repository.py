from abc import ABC, abstractmethod

from app.domain.entities import Medication


class MedicationRepository(ABC):
    """Puerto para acceso al catálogo de medicamentos. Las implementaciones pueden ser InMemory o Postgres."""

    @abstractmethod
    async def get_all(self) -> list[Medication]:
        """Devuelve todos los medicamentos del catálogo."""
        ...

    @abstractmethod
    async def get_by_id(self, id: str) -> Medication | None:
        """Obtiene un medicamento por id."""
        ...

    @abstractmethod
    async def get_available(self) -> list[Medication]:
        """Devuelve los medicamentos con stock disponible (o todos si no se filtra por stock)."""
        ...
