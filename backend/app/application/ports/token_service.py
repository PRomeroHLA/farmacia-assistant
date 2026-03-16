"""Puerto para creación y validación de tokens JWT. El caso de uso de login llama a create_token(user.id, user.username)."""

from abc import ABC, abstractmethod


class TokenService(ABC):
    """Interfaz para generar y decodificar tokens (p. ej. JWT)."""

    @abstractmethod
    def create_token(self, user_id: str, username: str, expiry_minutes: int = 60) -> str:
        """Genera un token que incluye al menos sub (user_id), username y exp. Para LoginResponse."""
        ...

    @abstractmethod
    def decode_token(self, token: str) -> dict | None:
        """Valida el token y devuelve el payload (sub, username, exp, ...) o None si inválido/expirado. Para get_current_user."""
        ...
