from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class FarmCondition(Base):
    __tablename__ = "farm_conditions"

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

    # Soil conditions
    soil_ph: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    soil_type: Mapped[str | None] = mapped_column(
    String(50),
    nullable=True,
)

    nitrogen: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    phosphorus: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    potassium: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    organic_matter: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    soil_moisture: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # Environmental conditions
    temperature: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    humidity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    rainfall: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    sunlight: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    farm = relationship(
        "Farm",
        back_populates="conditions",
    )