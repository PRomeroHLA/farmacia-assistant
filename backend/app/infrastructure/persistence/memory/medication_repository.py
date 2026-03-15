from app.application.ports import MedicationRepository
from app.domain.entities import Medication


class InMemoryMedicationRepository(MedicationRepository):
    """Implementación en memoria de MedicationRepository. Almacenamiento en dict por id."""

    def __init__(self, initial_medications: list[Medication] | None = None) -> None:
        self._by_id: dict[str, Medication] = {}
        for med in initial_medications or []:
            self._by_id[med.id] = med

    def get_all(self) -> list[Medication]:
        return list(self._by_id.values())

    def get_by_id(self, id: str) -> Medication | None:
        return self._by_id.get(id)

    def get_available(self) -> list[Medication]:
        """Devuelve medicamentos con stock (stock no None y distinto de '0'). Sin stock info se consideran disponibles."""
        return [
            m for m in self._by_id.values()
            if m.stock is None or m.stock.strip() == "" or m.stock != "0"
        ]
