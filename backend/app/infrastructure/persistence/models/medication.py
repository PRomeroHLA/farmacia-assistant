"""Modelos ORM SQLAlchemy para catálogo de medicamentos y stock (PostgreSQL)."""

from __future__ import annotations

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.models.base import Base


class MedicationModel(Base):
    __tablename__ = "medications"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # TEXT en PostgreSQL
    name: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(Text, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[str | None] = mapped_column(Text, nullable=True)
    format: Mapped[str | None] = mapped_column(Text, nullable=True)  # noqa: A003

    age_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    age_max: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Por simplicidad en el MVP: listas serializadas como TEXT con coma.
    # El repositorio parseará a tuple[str, ...].
    allowed_sexes: Mapped[str] = mapped_column(Text, nullable=False, default="")
    indicated_symptom_labels: Mapped[str] = mapped_column(Text, nullable=False, default="")
    indicated_hypothesis_labels: Mapped[str] = mapped_column(Text, nullable=False, default="")

    suitable_for_pregnancy: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    economic_margin: Mapped[object] = mapped_column(Numeric(10, 2), nullable=False, default=0)

    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    stock_row: Mapped["MedicationStockModel | None"] = relationship(
        back_populates="medication",
        uselist=False,
        cascade="all, delete-orphan",
    )


class MedicationStockModel(Base):
    __tablename__ = "medication_stock"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    medication_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("medications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    medication: Mapped[MedicationModel] = relationship(back_populates="stock_row")

