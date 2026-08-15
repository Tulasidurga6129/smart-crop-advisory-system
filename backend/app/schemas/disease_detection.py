from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DiseaseDetectionBase(BaseModel):
    disease_name: str = Field(
        min_length=1,
        max_length=150,
    )

    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    severity: str = Field(
        default="medium",
        max_length=20,
    )

    symptoms: str | None = None

    recommended_treatment: str | None = None

    preventive_measures: str | None = None

    detection_source: str = Field(
        default="manual",
        max_length=30,
    )

    status: str = Field(
        default="active",
        max_length=20,
    )


class DiseaseDetectionCreate(DiseaseDetectionBase):
    farm_id: int
    crop_id: int


class DiseaseDetectionUpdate(BaseModel):
    disease_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    severity: str | None = Field(
        default=None,
        max_length=20,
    )

    symptoms: str | None = None

    recommended_treatment: str | None = None

    preventive_measures: str | None = None

    detection_source: str | None = Field(
        default=None,
        max_length=30,
    )

    status: str | None = Field(
        default=None,
        max_length=20,
    )


class DiseaseDetectionResponse(DiseaseDetectionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    farm_id: int
    crop_id: int
    created_at: datetime
    updated_at: datetime
