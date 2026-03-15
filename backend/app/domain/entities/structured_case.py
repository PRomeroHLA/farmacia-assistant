from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from app.domain.entities.symptom import Symptom
from app.domain.entities.clinical_hypothesis import ClinicalHypothesis


@dataclass(frozen=True)
class StructuredCase:
    """Caso clínico ya estructurado: salida del análisis, entrada al motor de recomendaciones."""

    age: int | None
    sex: Literal["Hombre", "Mujer"] | None
    is_pregnant: bool
    symptoms: list[Symptom]
    hypotheses: list[ClinicalHypothesis]
