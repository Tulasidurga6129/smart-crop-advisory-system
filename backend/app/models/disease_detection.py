from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DiseaseDetection(Base):
    __tablename__ = "disease_detections"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    farm_id: Mapped[int] = mapped_column(
        ForeignKey(
            "farms.id",
            ondelete="CASCADE",
        ),
        nullable=False,
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

    disease_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="medium",
        index=True,
    )

    symptoms: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    recommended_treatment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    preventive_measures: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    detection_source: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="manual",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
        index=True,
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

    farm = relationship(
        "Farm",
        back_populates="disease_detections",
    )

    crop = relationship(
        "Crop",
        back_populates="disease_detections",
    )
