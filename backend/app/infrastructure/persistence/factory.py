"""Factory de repositorios según STORAGE_BACKEND. Usar con FastAPI Depends.

Usuario de prueba para login (solo STORAGE_BACKEND=memory):
  username: test
  contraseña: test123

Factory de repositorios según STORAGE_BACKEND. Usar con FastAPI Depends.

Con STORAGE_BACKEND=memory el catálogo de medicamentos usa datos de desarrollo
(get_default_medications). Con STORAGE_BACKEND=postgresql (video-07) se cargará desde la BD.
"""

from app.application.ports import (
    UserRepository,
    MedicationRepository,
    CaseRepository,
)
from app.domain.entities import User
from app.infrastructure.config import Settings
from app.infrastructure.persistence.memory import (
    InMemoryUserRepository,
    InMemoryMedicationRepository,
    InMemoryCaseRepository,
)
from app.infrastructure.security.password import hash_password
from app.infrastructure.persistence.memory.seed_medications import get_default_medications

# Singletons en memoria (pre-cargados con datos de ejemplo)
_memory_user_repo: InMemoryUserRepository | None = None
_memory_medication_repo: InMemoryMedicationRepository | None = None
_memory_case_repo: InMemoryCaseRepository | None = None


def _sample_users() -> list[User]:
    """Datos de ejemplo para desarrollo y pruebas. Incluye usuario de prueba para login.
    Usuario con password_hash real: username 'test', contraseña 'test123'.
    """
    test_password_hash = hash_password("test123")
    return [
        User(id="1", username="farmacia", full_name="Farmacia Centro", password_hash=None),
        User(id="2", username="admin", full_name="Administrador", password_hash=None),
        User(
            id="test-1",
            username="test",
            full_name="Usuario de prueba",
            password_hash=test_password_hash,
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
                initial_medications=get_default_medications()
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
