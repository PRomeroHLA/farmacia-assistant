"""Rutas de autenticación."""

from fastapi import APIRouter, Depends, HTTPException

from app.application.use_cases.login import InvalidCredentialsError, LoginUseCase
from app.interfaces.api.dependencies import get_login_use_case
from app.interfaces.api.schemas.auth import LoginRequest, LoginResponse, user_to_schema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(
    body: LoginRequest,
    login_use_case: LoginUseCase = Depends(get_login_use_case),
) -> LoginResponse:
    """Login con username y password. Devuelve user y token JWT o 401."""
    try:
        user, token = await login_use_case.run(username=body.username, password=body.password)
        return LoginResponse(user=user_to_schema(user), token=token)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
