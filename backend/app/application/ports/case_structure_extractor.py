"""Puerto para extraer la estructura clínica a partir del texto libre del caso. Implementaciones: mock, LLM en infrastructure."""

from abc import ABC, abstractmethod

from app.domain.entities import StructuredCase


class CaseStructureExtractor(ABC):
    """Interfaz para extraer StructuredCase desde texto libre. El caso de uso de análisis depende de esta interfaz por inyección."""

    @abstractmethod
    def extract(self, text: str) -> StructuredCase:
        """Recibe el texto libre del caso y devuelve la entidad StructuredCase (age, sex, is_pregnant, symptoms, hypotheses)."""
        ...
