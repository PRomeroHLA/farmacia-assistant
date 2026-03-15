"""Rutas de análisis de caso clínico."""

from fastapi import APIRouter, Depends

from app.application.use_cases.analyze_case import AnalyzeCaseUseCase
from app.interfaces.api.dependencies import get_analyze_case_use_case
from app.interfaces.api.schemas.case import (
    AnalyzeCaseRequest,
    StructuredCaseResponse,
    structured_case_to_response,
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
