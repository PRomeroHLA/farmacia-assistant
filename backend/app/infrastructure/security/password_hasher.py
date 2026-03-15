"""Implementación del puerto PasswordHasher usando bcrypt (algoritmo bcrypt). Inyectable en el caso de uso de login."""

from app.application.ports.password_hasher import PasswordHasher
from app.infrastructure.security.password import hash_password as _hash_password
from app.infrastructure.security.password import verify_password as _verify_password


class BcryptPasswordHasher(PasswordHasher):
    """Implementación con bcrypt. El login llamará a verify_password(contraseña_recibida, user.password_hash)."""

    def hash_password(self, plain: str) -> str:
        return _hash_password(plain)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return _verify_password(plain, hashed)
