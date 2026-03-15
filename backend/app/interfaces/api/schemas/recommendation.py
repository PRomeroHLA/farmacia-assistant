"""Schemas Pydantic para recomendaciones. Coinciden con frontend ProductRecommendation (recommendations.ts)."""

from typing import Literal

from pydantic import BaseModel

from app.domain.entities import Medication


class ProductRecommendation(BaseModel):
    """Recomendación de producto. Mismos campos que frontend ProductRecommendation."""

    id: str
    name: str
    category: str
    reason: str
    badge: Literal["main", "alternative"]
    price: str | None = None
    stock: str | None = None
    format: str | None = None  # noqa: A003


class RecommendationsResponse(BaseModel):
    """Respuesta del endpoint de recomendaciones: lista de productos y texto explicativo."""

    recommendations: list[ProductRecommendation]
    explanation: str


def medication_to_product_recommendation(medication: Medication) -> ProductRecommendation:
    """Convierte una entidad Medication del dominio al schema ProductRecommendation para la API.
    Solo incluye los campos que espera el frontend (id, name, category, reason, badge, price, stock, format).
    No expone economic_margin ni otros campos internos del catálogo.
    """
    return ProductRecommendation(
        id=medication.id,
        name=medication.name,
        category=medication.category,
        reason=medication.reason,
        badge=medication.badge,
        price=medication.price,
        stock=medication.stock,
        format=medication.format,
    )
