"""Rutas de análisis de caso clínico y recomendaciones."""

from fastapi import APIRouter, Depends, HTTPException

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
    RecommendationSymptomGroup,
    RecommendationsResponse,
    medication_to_product_recommendation,
)

router = APIRouter(prefix="/cases", tags=["cases"])


ANALYZE_ERROR_MESSAGE = "No se ha podido analizar el caso. Intente de nuevo más tarde."


@router.post("/analyze", response_model=StructuredCaseResponse)
def analyze_case(
    body: AnalyzeCaseRequest,
    analyze_case_use_case: AnalyzeCaseUseCase = Depends(get_analyze_case_use_case),
) -> StructuredCaseResponse:
    """Analiza el texto del caso y devuelve la estructura clínica (age, sex, isPregnant, symptoms, hypotheses)."""
    try:
        structured = analyze_case_use_case.run(body.text)
        return structured_case_to_response(structured)
    except Exception:
        # Cualquier fallo del extractor (mock, OpenAI, red, JSON inválido): respuesta genérica.
        # No se hace fallback a mock ni se exponen stack traces ni detalles internos.
        raise HTTPException(
            status_code=503,
            detail=ANALYZE_ERROR_MESSAGE,
        ) from None


RECOMMENDATIONS_EXPLANATION_PLACEHOLDER = "Recomendación según el caso clínico validado."


@router.post(
    "/recommendations",
    response_model=RecommendationsResponse,
    response_model_by_alias=True,
)
async def get_recommendations(
    body: StructuredCaseResponse,
    recommendations_use_case: RecommendationsUseCase = Depends(get_recommendations_use_case),
) -> RecommendationsResponse:
    """Recibe el caso clínico confirmado y devuelve recomendaciones (lista + explicación). La explicación es fija por ahora (video-08: LLM)."""
    case = request_body_to_structured_case(body)
    group_results = await recommendations_use_case.run(case)
    groups = [
        RecommendationSymptomGroup(
            symptom_label=g.symptom_label,
            recommendations=[
                medication_to_product_recommendation(
                    m,
                    case,
                    recommended_for_override=g.symptom_label,
                )
                for m in g.medications
            ],
        )
        for g in group_results
    ]
    return RecommendationsResponse(
        groups=groups,
        explanation=RECOMMENDATIONS_EXPLANATION_PLACEHOLDER,
    )
