from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NotificationBase(BaseModel):
    notification_type: str = Field(
        min_length=1,
        max_length=30,
    )

    title: str = Field(
        min_length=1,
        max_length=150,
    )

    message: str = Field(
        min_length=1,
    )

    priority: str = Field(
        default="medium",
        max_length=20,
    )


class NotificationCreate(NotificationBase):
    farm_id: int | None = None
    crop_id: int | None = None


class NotificationUpdate(BaseModel):
    notification_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=30,
    )

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    message: str | None = Field(
        default=None,
        min_length=1,
    )

    priority: str | None = Field(
        default=None,
        max_length=20,
    )


class NotificationResponse(NotificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    farm_id: int | None
    crop_id: int | None
    is_read: bool
    created_at: datetime
    read_at: datetime | None