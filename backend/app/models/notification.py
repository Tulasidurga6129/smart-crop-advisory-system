from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    farm_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "farms.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    crop_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "crops.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    notification_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="medium",
        index=True,
    )

    is_read: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    read_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    user = relationship(
        "User",
    )

    farm = relationship(
        "Farm",
    )

    crop = relationship(
        "Crop",
    )