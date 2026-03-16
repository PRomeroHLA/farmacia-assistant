"""Caso de uso de login. No exponer contraseña ni hash en logs ni respuestas."""

from app.application.ports.password_hasher import PasswordHasher
from app.application.ports.token_service import TokenService
from app.application.ports.user_repository import UserRepository
from app.domain.entities import User


class InvalidCredentialsError(Exception):
    """Credenciales inválidas (usuario no existe o contraseña incorrecta). El router puede mapear a HTTP 401."""

    pass


class LoginUseCase:
    """Login: verifica credenciales y devuelve (User, token). Dependencias inyectadas."""

    def __init__(
        self,
        *,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ) -> None:
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service

    def run(self, username: str, password: str) -> tuple[User, str]:
        """Ejecuta el login. Devuelve (user, token) o lanza InvalidCredentialsError."""
        user = self.user_repository.get_by_username(username)
        if user is None:
            raise InvalidCredentialsError()

        if user.password_hash is None or not self.password_hasher.verify_password(
            password, user.password_hash
        ):
            raise InvalidCredentialsError()

        token = self.token_service.create_token(user.id, user.username)
        return (user, token)
