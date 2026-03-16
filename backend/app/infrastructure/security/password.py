"""Hash y verificación de contraseñas (bcrypt). Usado por BcryptPasswordHasher y en seed de usuarios de prueba.
Algoritmo bcrypt; se usa la librería bcrypt (passlib[bcrypt] es equivalente si se prefiere)."""

import bcrypt


def hash_password(plain: str) -> str:
    """Devuelve el hash bcrypt de la contraseña en claro. Nunca almacenar plain en BD."""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("ascii")


def verify_password(plain: str, hashed: str) -> bool:
    """Comprueba si la contraseña en claro coincide con el hash (para login)."""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("ascii"))
