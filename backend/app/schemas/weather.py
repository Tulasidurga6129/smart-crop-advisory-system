from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WeatherBase(BaseModel):
    temperature: float | None = Field(
        default=None,
        description="Temperature in degrees Celsius",
    )

    humidity: float | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Relative humidity percentage",
    )

    rainfall: float | None = Field(
        default=None,
        ge=0,
        description="Rainfall in millimeters",
    )

    wind_speed: float | None = Field(
        default=None,
        ge=0,
        description="Wind speed in km/h",
    )

    weather_condition: str | None = Field(
        default=None,
        max_length=100,
    )

    observed_at: datetime | None = None


class WeatherCreate(WeatherBase):
    pass

class WeatherUpdate(BaseModel):
    temperature: float | None = Field(
        default=None,
        description="Temperature in degrees Celsius",
    )

    humidity: float | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Relative humidity percentage",
    )

    rainfall: float | None = Field(
        default=None,
        ge=0,
        description="Rainfall in millimeters",
    )

    wind_speed: float | None = Field(
        default=None,
        ge=0,
        description="Wind speed in km/h",
    )

    weather_condition: str | None = Field(
        default=None,
        max_length=100,
    )

    observed_at: datetime | None = None


class WeatherResponse(WeatherBase):
    id: int
    farm_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )