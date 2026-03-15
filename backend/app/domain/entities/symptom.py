from dataclasses import dataclass


@dataclass(frozen=True)
class Symptom:
    """Síntoma detectado en el caso clínico (ej. 'Dolor de garganta'). Se usa dentro de StructuredCase."""

    id: str
    label: str
