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
from app.infrastructure.persistence.models.engine import get_async_engine, get_async_session_maker
from app.infrastructure.persistence.postgres import (
    PostgresMedicationRepository,
    PostgresUserRepository,
)
from app.infrastructure.security.password import hash_password
from app.infrastructure.persistence.memory.seed_medications import get_default_medications

# Singletons en memoria (pre-cargados con datos de ejemplo)
_memory_user_repo: InMemoryUserRepository | None = None
_memory_medication_repo: InMemoryMedicationRepository | None = None
_memory_case_repo: InMemoryCaseRepository | None = None

# Singletons PostgreSQL (engine/sessionmaker + repos)
_pg_engine = None
_pg_session_maker = None
_pg_user_repo: PostgresUserRepository | None = None
_pg_medication_repo: PostgresMedicationRepository | None = None


def _get_pg_session_maker(settings: Settings):
    """Crea/reutiliza engine y sessionmaker async para PostgreSQL."""
    global _pg_engine, _pg_session_maker
    if settings.DATABASE_URL is None or settings.DATABASE_URL.strip() == "":
        raise ValueError(
            'DATABASE_URL es obligatoria cuando STORAGE_BACKEND="postgresql" '
            '(ej. postgresql+asyncpg://user:password@localhost:5432/farmacia_db)'
        )
    if _pg_engine is None or _pg_session_maker is None:
        _pg_engine = get_async_engine(settings.DATABASE_URL)
        _pg_session_maker = get_async_session_maker(_pg_engine)
    return _pg_session_maker


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
        global _pg_user_repo
        if _pg_user_repo is None:
            session_maker = _get_pg_session_maker(settings)
            _pg_user_repo = PostgresUserRepository(session_maker)
        return _pg_user_repo
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
        global _pg_medication_repo
        if _pg_medication_repo is None:
            session_maker = _get_pg_session_maker(settings)
            _pg_medication_repo = PostgresMedicationRepository(session_maker)
        return _pg_medication_repo
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
