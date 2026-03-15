from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.config import get_settings
from app.interfaces.api.routes.cases import router as cases_router
from app.interfaces.api.routes.routers import router as api_router

app = FastAPI(
    title="Asistente de Recomendación Farmacéutica",
    description="API del backend para apoyo a la recomendación de medicamentos a partir de casos clínicos.",
)

_settings = get_settings()
_cors_origins = [o.strip() for o in _settings.CORS_ORIGINS.split(",") if o.strip()] or ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(cases_router)
