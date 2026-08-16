from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FarmConditionBase(BaseModel):
    soil_ph: float | None = Field(
        default=None,
        ge=0,
        le=14,
    )
    soil_type: str | None = Field(
        default=None,
        max_length=50,
    )


    nitrogen: float | None = Field(
        default=None,
        ge=0,
    )

    phosphorus: float | None = Field(
        default=None,
        ge=0,
    )

    potassium: float | None = Field(
        default=None,
        ge=0,
    )

    organic_matter: float | None = Field(
        default=None,
        ge=0,
    )

    soil_moisture: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    temperature: float | None = None

    humidity: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    rainfall: float | None = Field(
        default=None,
        ge=0,
    )

    sunlight: float | None = Field(
        default=None,
        ge=0,
    )


class FarmConditionCreate(FarmConditionBase):
    pass


class FarmConditionUpdate(FarmConditionBase):
    pass


class FarmConditionResponse(FarmConditionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    farm_id: int
    recorded_at: datetime
    created_at: datetime