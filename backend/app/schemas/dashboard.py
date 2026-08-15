from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class DashboardFarmResponse(BaseModel):
    id: int
    farm_name: str
    location: str | None
    village: str | None
    district: str | None
    state: str | None
    land_area: float
    land_unit: str
    soil_type: str | None
    irrigation_type: str | None
    current_crop: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class DashboardCropResponse(BaseModel):
    id: int
    name: str
    variety: str | None
    season: str
    sowing_date: date | None
    expected_harvest_date: date | None
    area: float | None
    status: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class DashboardConditionResponse(BaseModel):
    id: int
    soil_ph: float | None
    nitrogen: float | None
    phosphorus: float | None
    potassium: float | None
    organic_matter: float | None
    soil_moisture: float | None
    temperature: float | None
    humidity: float | None
    rainfall: float | None
    sunlight: float | None
    recorded_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class DashboardWeatherResponse(BaseModel):
    id: int
    temperature: float | None
    humidity: float | None
    rainfall: float | None
    wind_speed: float | None
    weather_condition: str | None
    observed_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class DashboardAdvisoryResponse(BaseModel):
    id: int
    crop_id: int
    advisory_type: str
    title: str
    message: str
    priority: str
    status: str
    valid_until: datetime | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class DashboardSummaryResponse(BaseModel):
    high: int
    medium: int
    low: int
    total: int
    top_priority: str | None


class FarmDashboardResponse(BaseModel):
    farm: DashboardFarmResponse
    crops: list[DashboardCropResponse]
    latest_condition: DashboardConditionResponse | None
    latest_weather: DashboardWeatherResponse | None
    active_advisories: list[DashboardAdvisoryResponse]
    summary: DashboardSummaryResponse