# FastAPI dependencies (Depends)

from fastapi import Depends

from app.application.ports import UserRepository, MedicationRepository, CaseRepository
from app.application.use_cases.analyze_case import AnalyzeCaseUseCase
from app.infrastructure.config import get_settings
from app.infrastructure.config import Settings
from app.infrastructure.llm import MockCaseStructureExtractor
from app.infrastructure.persistence.factory import (
    get_user_repository as _get_user_repository,
    get_medication_repository as _get_medication_repository,
    get_case_repository as _get_case_repository,
)


def get_user_repository(
    settings: Settings = Depends(get_settings),
) -> UserRepository:
    """Inyecta UserRepository según STORAGE_BACKEND. Uso: Depends(get_user_repository)."""
    return _get_user_repository(settings)


def get_medication_repository(
    settings: Settings = Depends(get_settings),
) -> MedicationRepository:
    """Inyecta MedicationRepository según STORAGE_BACKEND. Uso: Depends(get_medication_repository)."""
    return _get_medication_repository(settings)


def get_case_repository(
    settings: Settings = Depends(get_settings),
) -> CaseRepository:
    """Inyecta CaseRepository según STORAGE_BACKEND. Uso: Depends(get_case_repository)."""
    return _get_case_repository(settings)


def get_analyze_case_use_case() -> AnalyzeCaseUseCase:
    """Inyecta AnalyzeCaseUseCase con MockCaseStructureExtractor."""
    return AnalyzeCaseUseCase(case_structure_extractor=MockCaseStructureExtractor())
