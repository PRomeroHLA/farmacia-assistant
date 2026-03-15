"""Schemas Pydantic para caso clínico. Salida en camelCase donde aplique (frontend clinical.ts)."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities import ClinicalHypothesis, StructuredCase, Symptom


class SymptomSchema(BaseModel):
    """Síntoma detectado. Mismo formato que frontend Symptom."""

    id: str
    label: str


class ClinicalHypothesisSchema(BaseModel):
    """Hipótesis clínica. Mismo formato que frontend ClinicalHypothesis."""

    id: str
    label: str


class StructuredCaseResponse(BaseModel):
    """Respuesta del backend al analizar el caso. isPregnant en camelCase."""

    model_config = ConfigDict(populate_by_name=True)

    age: int | None = None
    sex: Literal["Hombre", "Mujer"] | None = None
    is_pregnant: bool = Field(False, alias="isPregnant")
    symptoms: list[SymptomSchema] = []
    hypotheses: list[ClinicalHypothesisSchema] = []


class AnalyzeCaseRequest(BaseModel):
    """Body de la petición de análisis: texto libre del caso."""

    text: str


def structured_case_to_response(case: StructuredCase) -> StructuredCaseResponse:
    """Mapea la entidad StructuredCase al schema de API (StructuredCaseResponse)."""
    return StructuredCaseResponse(
        age=case.age,
        sex=case.sex,
        is_pregnant=case.is_pregnant,
        symptoms=[SymptomSchema(id=s.id, label=s.label) for s in case.symptoms],
        hypotheses=[ClinicalHypothesisSchema(id=h.id, label=h.label) for h in case.hypotheses],
    )


def request_body_to_structured_case(body: StructuredCaseResponse) -> StructuredCase:
    """Convierte el body de la petición (caso confirmado) a la entidad StructuredCase.
    El body tiene la misma estructura que StructuredCaseResponse (age, sex, isPregnant, symptoms, hypotheses).
    """
    return StructuredCase(
        age=body.age,
        sex=body.sex,
        is_pregnant=body.is_pregnant,
        symptoms=[Symptom(id=s.id, label=s.label) for s in body.symptoms],
        hypotheses=[ClinicalHypothesis(id=h.id, label=h.label) for h in body.hypotheses],
    )
