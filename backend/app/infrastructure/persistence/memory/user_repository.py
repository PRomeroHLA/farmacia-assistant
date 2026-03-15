from app.application.ports import UserRepository
from app.domain.entities import User


class InMemoryUserRepository(UserRepository):
    """Implementación en memoria de UserRepository. Solo estructuras Python (dict)."""

    def __init__(self, initial_users: list[User] | None = None) -> None:
        self._by_id: dict[str, User] = {}
        self._by_username: dict[str, User] = {}
        for user in initial_users or []:
            self.add(user)

    def get_by_username(self, username: str) -> User | None:
        return self._by_username.get(username)

    def get_by_id(self, id: str) -> User | None:
        return self._by_id.get(id)

    def add(self, user: User) -> None:
        # Permitir actualizar si ya existe (mismo id)
        if user.id in self._by_id:
            old = self._by_id[user.id]
            if old.username != user.username:
                del self._by_username[old.username]
        self._by_id[user.id] = user
        self._by_username[user.username] = user
