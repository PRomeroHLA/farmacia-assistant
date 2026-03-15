# Pydantic schemas (request/response DTOs for API)

from app.interfaces.api.schemas.auth import LoginRequest, LoginResponse, UserSchema
from app.interfaces.api.schemas.case import (
    SymptomSchema,
    ClinicalHypothesisSchema,
    StructuredCaseResponse,
    AnalyzeCaseRequest,
)
from app.interfaces.api.schemas.recommendation import ProductRecommendation

__all__ = [
    "LoginRequest",
    "LoginResponse",
    "UserSchema",
    "SymptomSchema",
    "ClinicalHypothesisSchema",
    "StructuredCaseResponse",
    "AnalyzeCaseRequest",
    "ProductRecommendation",
]
