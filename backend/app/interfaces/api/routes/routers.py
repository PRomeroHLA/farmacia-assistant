from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Comprueba que el servicio está en marcha."""
    return {"status": "ok"}
