"""Tests de contrato para schemas de recomendaciones. Alineados con frontend recommendations.ts."""

import pytest
from pydantic import ValidationError

from app.interfaces.api.schemas.recommendation import ProductRecommendation


def test_product_recommendation_has_required_fields():
    """ProductRecommendation: id, name, category, reason, badge (main|alternative)."""
    p = ProductRecommendation(
        id="med-1",
        name="Paracetamol 500 mg",
        category="Analgésico",
        reason="Dolor leve",
        badge="main",
    )
    data = p.model_dump(by_alias=True)
    assert data["id"] == "med-1"
    assert data["name"] == "Paracetamol 500 mg"
    assert data["category"] == "Analgésico"
    assert data["reason"] == "Dolor leve"
    assert data["badge"] == "main"


def test_product_recommendation_optional_fields():
    """ProductRecommendation: price, stock, format opcionales."""
    p = ProductRecommendation(
        id="med-2",
        name="Ibuprofeno",
        category="Antiinflamatorio",
        reason="Inflamación",
        badge="alternative",
        price="4.20",
        stock="50",
        format="30 comprimidos",
    )
    data = p.model_dump(by_alias=True)
    assert data.get("price") == "4.20"
    assert data.get("stock") == "50"
    assert data.get("format") == "30 comprimidos"


def test_product_recommendation_badge_only_main_or_alternative():
    """badge solo acepta 'main' o 'alternative'."""
    for badge in ("main", "alternative"):
        p = ProductRecommendation(
            id="x", name="X", category="Y", reason="Z", badge=badge,
        )
        assert p.model_dump(by_alias=True)["badge"] == badge

    with pytest.raises(ValidationError):
        ProductRecommendation(
            id="x", name="X", category="Y", reason="Z", badge="invalid",
        )
