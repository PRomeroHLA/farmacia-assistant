"""Caso de uso de análisis de caso: extrae la estructura clínica desde texto libre."""

from app.application.ports.case_structure_extractor import CaseStructureExtractor
from app.domain.entities import StructuredCase


class AnalyzeCaseUseCase:
    """Analiza el texto del caso y devuelve StructuredCase. Depende de CaseStructureExtractor por inyección."""

    def __init__(self, *, case_structure_extractor: CaseStructureExtractor) -> None:
        self.case_structure_extractor = case_structure_extractor

    def run(self, text: str) -> StructuredCase:
        """Ejecuta la extracción: delega en el extractor y devuelve el StructuredCase."""
        return self.case_structure_extractor.extract(text)
