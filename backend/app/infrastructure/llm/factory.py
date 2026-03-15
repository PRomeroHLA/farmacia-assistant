"""Factory para elegir la implementación de CaseStructureExtractor según configuración (LLM_EXTRACTOR)."""

from app.application.ports.case_structure_extractor import CaseStructureExtractor
from app.infrastructure.config import Settings
from app.infrastructure.llm.mock_case_structure_extractor import MockCaseStructureExtractor
from app.infrastructure.llm.openai_case_structure_extractor import OpenAICaseStructureExtractor


def get_case_structure_extractor(settings: Settings) -> CaseStructureExtractor:
    """Devuelve MockCaseStructureExtractor si LLM_EXTRACTOR==\"mock\", o OpenAICaseStructureExtractor
    configurado con OPENAI_API_KEY y OPENAI_MODEL si LLM_EXTRACTOR==\"openai\".
    Con \"openai\" debe definirse OPENAI_API_KEY (no None ni vacía); si no, se lanza ValueError.
    """
    if settings.LLM_EXTRACTOR == "mock":
        return MockCaseStructureExtractor()
    if settings.LLM_EXTRACTOR == "openai":
        api_key = settings.OPENAI_API_KEY
        if not api_key or not str(api_key).strip():
            raise ValueError(
                "LLM_EXTRACTOR=openai requiere OPENAI_API_KEY definida y no vacía en la configuración."
            )
        return OpenAICaseStructureExtractor(
            api_key=api_key.strip(),
            model=settings.OPENAI_MODEL,
        )
    raise ValueError(f"LLM_EXTRACTOR no soportado: {settings.LLM_EXTRACTOR}")
