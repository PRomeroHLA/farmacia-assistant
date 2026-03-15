# FastAPI dependencies (Depends)

from fastapi import Depends

from app.application.ports import (
    UserRepository,
    MedicationRepository,
    CaseRepository,
    PasswordHasher,
    TokenService,
)
from app.application.use_cases.login import LoginUseCase
from app.infrastructure.config import get_settings
from app.infrastructure.config import Settings
from app.infrastructure.persistence.factory import (
    get_user_repository as _get_user_repository,
    get_medication_repository as _get_medication_repository,
    get_case_repository as _get_case_repository,
)
from app.infrastructure.security import BcryptPasswordHasher, JWTTokenService


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


def get_password_hasher() -> PasswordHasher:
    """Inyecta PasswordHasher (Bcrypt)."""
    return BcryptPasswordHasher()


def get_token_service(
    settings: Settings = Depends(get_settings),
) -> TokenService:
    """Inyecta TokenService (JWT)."""
    return JWTTokenService(settings)


def get_login_use_case(
    user_repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
    token_service: TokenService = Depends(get_token_service),
) -> LoginUseCase:
    """Inyecta LoginUseCase con dependencias configuradas."""
    return LoginUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        token_service=token_service,
    )
