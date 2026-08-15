from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CropMonitoring(Base):
    __tablename__ = "crop_monitoring"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    crop_id: Mapped[int] = mapped_column(
        ForeignKey(
            "crops.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    monitoring_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    growth_stage: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    plant_height: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    crop_health: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    pest_observed: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    disease_observed: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    observation_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    crop = relationship(
        "Crop",
        back_populates="monitoring_records",
    )