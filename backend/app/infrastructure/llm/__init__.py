# Clientes externos LLM (mock y futuras implementaciones reales)

from app.infrastructure.llm.mock_case_structure_extractor import MockCaseStructureExtractor
from app.infrastructure.llm.openai_case_structure_extractor import (
    CaseStructureExtractionError,
    OpenAICaseStructureExtractor,
)

__all__ = [
    "MockCaseStructureExtractor",
    "OpenAICaseStructureExtractor",
    "CaseStructureExtractionError",
]
