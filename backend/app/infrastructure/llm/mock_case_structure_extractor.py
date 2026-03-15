"""Mock de CaseStructureExtractor. Sin llamadas a LLM; devuelve siempre un StructuredCase de ejemplo coherente con el frontend."""

from app.application.ports.case_structure_extractor import CaseStructureExtractor
from app.domain.entities import ClinicalHypothesis, StructuredCase, Symptom


# Caso de ejemplo fijo para tests y flujo con el frontend (clinical.ts)
_DEFAULT_CASE = StructuredCase(
    age=35,
    sex="Mujer",
    is_pregnant=False,
    symptoms=[
        Symptom(id="sym-1", label="Dolor de garganta"),
        Symptom(id="sym-2", label="Fiebre leve"),
    ],
    hypotheses=[
        ClinicalHypothesis(id="hyp-1", label="Faringitis leve"),
    ],
)


class MockCaseStructureExtractor(CaseStructureExtractor):
    """Implementación mock: ignora el texto y devuelve siempre un StructuredCase de ejemplo."""

    def extract(self, text: str) -> StructuredCase:
        return _DEFAULT_CASE
