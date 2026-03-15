"""Factory de repositorios según STORAGE_BACKEND. Usar con FastAPI Depends."""

from app.application.ports import (
    UserRepository,
    MedicationRepository,
    CaseRepository,
)
from app.domain.entities import User, Medication
from app.infrastructure.config import Settings
from app.infrastructure.persistence.memory import (
    InMemoryUserRepository,
    InMemoryMedicationRepository,
    InMemoryCaseRepository,
)

# Singletons en memoria (pre-cargados con datos de ejemplo)
_memory_user_repo: InMemoryUserRepository | None = None
_memory_medication_repo: InMemoryMedicationRepository | None = None
_memory_case_repo: InMemoryCaseRepository | None = None


def _sample_users() -> list[User]:
    """Datos de ejemplo para desarrollo y pruebas."""
    return [
        User(id="1", username="farmacia", full_name="Farmacia Centro"),
        User(id="2", username="admin", full_name="Administrador"),
    ]


def _sample_medications() -> list[Medication]:
    """Medicamentos de ejemplo para desarrollo y pruebas."""
    return [
        Medication(
            id="med-1",
            name="Paracetamol 500 mg",
            category="Analgésico",
            reason="Dolor leve, fiebre",
            badge="main",
            price="3.50",
            stock="100",
            format="20 comprimidos",
        ),
        Medication(
            id="med-2",
            name="Ibuprofeno 400 mg",
            category="Antiinflamatorio",
            reason="Dolor, inflamación",
            badge="alternative",
            price="4.20",
            stock="50",
            format="30 comprimidos",
        ),
    ]


def get_user_repository(settings: Settings) -> UserRepository:
    """Devuelve el UserRepository según STORAGE_BACKEND. Para uso con Depends(get_user_repository)."""
    global _memory_user_repo
    if settings.STORAGE_BACKEND == "memory":
        if _memory_user_repo is None:
            _memory_user_repo = InMemoryUserRepository(initial_users=_sample_users())
        return _memory_user_repo
    if settings.STORAGE_BACKEND == "postgresql":
        raise NotImplementedError(
            "PostgreSQL UserRepository se implementará en video-04 (modelos y migraciones)."
        )
    raise ValueError(f"STORAGE_BACKEND no soportado: {settings.STORAGE_BACKEND}")


def get_medication_repository(settings: Settings) -> MedicationRepository:
    """Devuelve el MedicationRepository según STORAGE_BACKEND. Para uso con Depends(get_medication_repository)."""
    global _memory_medication_repo
    if settings.STORAGE_BACKEND == "memory":
        if _memory_medication_repo is None:
            _memory_medication_repo = InMemoryMedicationRepository(
                initial_medications=_sample_medications()
            )
        return _memory_medication_repo
    if settings.STORAGE_BACKEND == "postgresql":
        raise NotImplementedError(
            "PostgreSQL MedicationRepository se implementará en video-04."
        )
    raise ValueError(f"STORAGE_BACKEND no soportado: {settings.STORAGE_BACKEND}")


def get_case_repository(settings: Settings) -> CaseRepository:
    """Devuelve el CaseRepository según STORAGE_BACKEND. Para uso con Depends(get_case_repository)."""
    global _memory_case_repo
    if settings.STORAGE_BACKEND == "memory":
        if _memory_case_repo is None:
            _memory_case_repo = InMemoryCaseRepository()
        return _memory_case_repo
    if settings.STORAGE_BACKEND == "postgresql":
        raise NotImplementedError(
            "PostgreSQL CaseRepository se implementará en video-04."
        )
    raise ValueError(f"STORAGE_BACKEND no soportado: {settings.STORAGE_BACKEND}")
