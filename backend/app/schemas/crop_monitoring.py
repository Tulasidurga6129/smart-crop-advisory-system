from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class CropMonitoringCreate(BaseModel):
    crop_id: int
    monitoring_date: date
    growth_stage: str = Field(..., min_length=1, max_length=100)
    plant_height: float | None = Field(default=None, ge=0)
    crop_health: str | None = Field(default=None, max_length=50)
    pest_observed: bool = False
    disease_observed: bool = False
    observation_notes: str | None = None


class CropMonitoringUpdate(BaseModel):
    monitoring_date: date | None = None
    growth_stage: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    plant_height: float | None = Field(default=None, ge=0)
    crop_health: str | None = Field(default=None, max_length=50)
    pest_observed: bool | None = None
    disease_observed: bool | None = None
    observation_notes: str | None = None


class CropMonitoringResponse(BaseModel):
    id: int
    crop_id: int
    monitoring_date: date
    growth_stage: str
    plant_height: float | None
    crop_health: str | None
    pest_observed: bool
    disease_observed: bool
    observation_notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )