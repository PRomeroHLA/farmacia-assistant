from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """Usuario del sistema (auth). Los repositorios devuelven y reciben User.
    password_hash nunca se expone en la API; solo se usa para verificar en login.
    """

    id: str
    username: str
    full_name: str | None = None
    password_hash: str | None = None
