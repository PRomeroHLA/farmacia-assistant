from dataclasses import dataclass


@dataclass(frozen=True)
class ClinicalHypothesis:
    """Hipótesis clínica orientativa (ej. 'Faringitis leve'). Se usa dentro de StructuredCase."""

    id: str
    label: str
