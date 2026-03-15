# Pydantic schemas (request/response DTOs for API)

from app.interfaces.api.schemas.auth import LoginRequest, LoginResponse, UserSchema
from app.interfaces.api.schemas.case import (
    SymptomSchema,
    ClinicalHypothesisSchema,
    StructuredCaseResponse,
    AnalyzeCaseRequest,
    request_body_to_structured_case,
)
from app.interfaces.api.schemas.recommendation import (
    ProductRecommendation,
    RecommendationsResponse,
    medication_to_product_recommendation,
)

__all__ = [
    "LoginRequest",
    "LoginResponse",
    "UserSchema",
    "SymptomSchema",
    "ClinicalHypothesisSchema",
    "StructuredCaseResponse",
    "AnalyzeCaseRequest",
    "request_body_to_structured_case",
    "ProductRecommendation",
    "RecommendationsResponse",
    "medication_to_product_recommendation",
]
