from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Farm(Base):
    __tablename__ = "farms"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    farmer_profile_id: Mapped[int] = mapped_column(
        ForeignKey(
            "farmer_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    farm_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    village: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    district: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    land_area: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    land_unit: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="acres",
    )

    soil_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    irrigation_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    current_crop: Mapped[str | None] = mapped_column(
        String(100),
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

    farmer_profile = relationship(
        "FarmerProfile",
        back_populates="farms",
    )