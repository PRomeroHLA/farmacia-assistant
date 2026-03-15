"""Rutas de análisis de caso clínico y recomendaciones."""

from fastapi import APIRouter, Depends

from app.application.use_cases.analyze_case import AnalyzeCaseUseCase
from app.application.use_cases.recommendations import RecommendationsUseCase
from app.interfaces.api.dependencies import get_analyze_case_use_case, get_recommendations_use_case
from app.interfaces.api.schemas.case import (
    AnalyzeCaseRequest,
    StructuredCaseResponse,
    request_body_to_structured_case,
    structured_case_to_response,
)
from app.interfaces.api.schemas.recommendation import (
    ProductRecommendation,
    RecommendationsResponse,
    medication_to_product_recommendation,
)

router = APIRouter(prefix="/cases", tags=["cases"])


@router.post("/analyze", response_model=StructuredCaseResponse)
def analyze_case(
    body: AnalyzeCaseRequest,
    analyze_case_use_case: AnalyzeCaseUseCase = Depends(get_analyze_case_use_case),
) -> StructuredCaseResponse:
    """Analiza el texto del caso y devuelve la estructura clínica (age, sex, isPregnant, symptoms, hypotheses)."""
    structured = analyze_case_use_case.run(body.text)
    return structured_case_to_response(structured)


RECOMMENDATIONS_EXPLANATION_PLACEHOLDER = "Recomendación según el caso clínico validado."


@router.post("/recommendations", response_model=RecommendationsResponse)
def get_recommendations(
    body: StructuredCaseResponse,
    recommendations_use_case: RecommendationsUseCase = Depends(get_recommendations_use_case),
) -> RecommendationsResponse:
    """Recibe el caso clínico confirmado y devuelve recomendaciones (lista + explicación). La explicación es fija por ahora (video-08: LLM)."""
    case = request_body_to_structured_case(body)
    medications = recommendations_use_case.run(case)
    recommendations = [medication_to_product_recommendation(m) for m in medications]
    return RecommendationsResponse(
        recommendations=recommendations,
        explanation=RECOMMENDATIONS_EXPLANATION_PLACEHOLDER,
    )
