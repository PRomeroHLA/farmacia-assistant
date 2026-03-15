"""Puerto para hash y verificación de contraseñas. El caso de uso de login usa verify_password(plain, user.password_hash)."""

from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Interfaz para hashear y verificar contraseñas. Nunca comparar en claro ni almacenar la contraseña."""

    @abstractmethod
    def hash_password(self, plain: str) -> str:
        """Devuelve el hash de la contraseña en claro. Para almacenar en User.password_hash."""
        ...

    @abstractmethod
    def verify_password(self, plain: str, hashed: str) -> bool:
        """Comprueba si la contraseña en claro coincide con el hash. Para login: verify_password(contraseña_recibida, user.password_hash)."""
        ...
