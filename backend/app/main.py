from fastapi import FastAPI

from app.interfaces.api.routes.auth import router as auth_router
from app.interfaces.api.routes.routers import router as api_router

app = FastAPI(
    title="Asistente de Recomendación Farmacéutica",
    description="API del backend para apoyo a la recomendación de medicamentos a partir de casos clínicos.",
)

app.include_router(api_router)
app.include_router(auth_router)
