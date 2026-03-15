import uuid

from app.application.ports import CaseRepository
from app.domain.entities import StructuredCase


class InMemoryCaseRepository(CaseRepository):
    """Implementación en memoria de CaseRepository. Almacenamiento en dict por id generado."""

    def __init__(self, initial_cases: dict[str, StructuredCase] | None = None) -> None:
        self._by_id: dict[str, StructuredCase] = dict(initial_cases or {})

    def save(self, case: StructuredCase) -> str:
        id_ = str(uuid.uuid4())
        self._by_id[id_] = case
        return id_

    def get_by_id(self, id: str) -> StructuredCase | None:
        return self._by_id.get(id)
