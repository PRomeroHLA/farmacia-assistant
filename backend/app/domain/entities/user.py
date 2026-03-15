from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """Usuario del sistema (auth). Los repositorios devuelven y reciben User."""

    id: str
    username: str
    full_name: str | None = None
