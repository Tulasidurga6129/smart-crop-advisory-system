from datetime import date

from pydantic import BaseModel, Field


class CropCreate(BaseModel):
    farm_id: int = Field(
        ...,
        gt=0,
    )

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    variety: str | None = Field(
        default=None,
        max_length=100,
    )

    season: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    sowing_date: date | None = None

    expected_harvest_date: date | None = None

    area: float | None = Field(
        default=None,
        gt=0,
    )

    status: str = Field(
        default="planned",
        max_length=50,
    )


class CropUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    variety: str | None = Field(
        default=None,
        max_length=100,
    )

    season: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    sowing_date: date | None = None

    expected_harvest_date: date | None = None

    area: float | None = Field(
        default=None,
        gt=0,
    )

    status: str | None = Field(
        default=None,
        max_length=50,
    )


class CropResponse(BaseModel):
    id: int
    farm_id: int
    name: str
    variety: str | None
    season: str
    sowing_date: date | None
    expected_harvest_date: date | None
    area: float | None
    status: str

    crop_age_days: int | None = None
    growth_stage: str | None = None
    days_to_harvest: int | None = None

    model_config = {
        "from_attributes": True
    }