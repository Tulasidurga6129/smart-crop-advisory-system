from datetime import datetime

from pydantic import BaseModel, Field


class FarmerProfileCreate(BaseModel):
    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    address: str | None = Field(
        default=None,
        max_length=255,
    )

    village: str | None = Field(
        default=None,
        max_length=100,
    )

    district: str | None = Field(
        default=None,
        max_length=100,
    )

    state: str | None = Field(
        default=None,
        max_length=100,
    )

    land_area: float | None = Field(
        default=None,
        gt=0,
    )

    land_unit: str | None = Field(
        default=None,
        max_length=20,
    )

    primary_crop: str | None = Field(
        default=None,
        max_length=100,
    )


class FarmerProfileUpdate(BaseModel):
    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    address: str | None = Field(
        default=None,
        max_length=255,
    )

    village: str | None = Field(
        default=None,
        max_length=100,
    )

    district: str | None = Field(
        default=None,
        max_length=100,
    )

    state: str | None = Field(
        default=None,
        max_length=100,
    )

    land_area: float | None = Field(
        default=None,
        gt=0,
    )

    land_unit: str | None = Field(
        default=None,
        max_length=20,
    )

    primary_crop: str | None = Field(
        default=None,
        max_length=100,
    )


class FarmerProfileResponse(BaseModel):
    id: int
    user_id: int
    phone: str | None
    address: str | None
    village: str | None
    district: str | None
    state: str | None
    land_area: float | None
    land_unit: str | None
    primary_crop: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }