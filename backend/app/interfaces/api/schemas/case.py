"""Schemas Pydantic para caso clínico. Salida en camelCase donde aplique (frontend clinical.ts)."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


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
