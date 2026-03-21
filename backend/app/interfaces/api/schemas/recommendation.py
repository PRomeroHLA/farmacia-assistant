"""Schemas Pydantic para recomendaciones. Coinciden con frontend ProductRecommendation (recommendations.ts)."""

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities import Medication, StructuredCase
from app.domain.services.recommendation_rules import matching_recommendation_label


class ProductRecommendation(BaseModel):
    """Recomendación de producto. Mismos campos que frontend ProductRecommendation."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    category: str
    reason: str
    badge: Literal["main", "alternative"]
    price: str | None = None
    stock: str | None = None
    format: str | None = None  # noqa: A003
    recommended_for: str | None = Field(default=None, serialization_alias="recommendedFor")
    commercial_margin: str | None = Field(default=None, serialization_alias="commercialMargin")
    stock_units: str | None = Field(default=None, serialization_alias="stockUnits")


class RecommendationSymptomGroup(BaseModel):
    """Bloque de recomendaciones por síntoma (orden del caso); dentro, productos por margen desc."""

    model_config = ConfigDict(populate_by_name=True)

    symptom_label: str | None = Field(default=None, serialization_alias="symptomLabel")
    recommendations: list[ProductRecommendation]


class RecommendationsResponse(BaseModel):
    """Respuesta del endpoint: grupos por síntoma (3 productos/síntoma) + explicación."""

    model_config = ConfigDict(populate_by_name=True)

    groups: list[RecommendationSymptomGroup]
    explanation: str


def _parse_stock_units_int(medication: Medication) -> int | None:
    if medication.stock_quantity is not None:
        return medication.stock_quantity
    raw = medication.stock
    if raw is None or not str(raw).strip().isdigit():
        return None
    return int(str(raw).strip())


def _stock_status_from_units(units: int) -> str:
    """Alineado con persistencia PostgreSQL (_stock_label): umbral pocas unidades ≤5."""
    if units <= 0:
        return "Sin stock"
    if units <= 5:
        return "Pocas unidades"
    return "En stock"


def _stock_fields_for_api(medication: Medication) -> tuple[str | None, str | None]:
    """(estado de stock para la UI, unidades como string o None)."""
    units = _parse_stock_units_int(medication)
    if units is not None:
        return _stock_status_from_units(units), str(units)
    return (medication.stock.strip() if medication.stock else None), None


def _format_commercial_margin(value: Decimal) -> str:
    q = value.quantize(Decimal("0.01"))
    text = format(q, "f")
    return f"{text.replace('.', ',')} €"


def medication_to_product_recommendation(
    medication: Medication,
    case: StructuredCase,
    *,
    recommended_for_override: str | None = None,
) -> ProductRecommendation:
    """Convierte Medication + caso confirmado al DTO de API (incluye etiqueta clínica y margen)."""
    stock_status, stock_units = _stock_fields_for_api(medication)
    margin_str = _format_commercial_margin(medication.economic_margin)
    rf = (
        matching_recommendation_label(case, medication)
        if recommended_for_override is None
        else recommended_for_override
    )
    return ProductRecommendation(
        id=medication.id,
        name=medication.name,
        category=medication.category,
        reason=medication.reason,
        badge=medication.badge,
        price=medication.price,
        stock=stock_status,
        format=medication.format,
        recommended_for=rf,
        commercial_margin=margin_str,
        stock_units=stock_units,
    )
