from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Crop(Base):
    __tablename__ = "crops"

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

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    variety: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    season: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    sowing_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    expected_harvest_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    area: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="planned",
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
        back_populates="crops",
    )
    advisories = relationship(
        "CropAdvisory",
        back_populates="crop",
        cascade="all, delete-orphan",
    )
    disease_detections = relationship(
        "DiseaseDetection",
        back_populates="crop",
        cascade="all, delete-orphan",
    )