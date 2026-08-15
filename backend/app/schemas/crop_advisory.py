from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CropAdvisoryBase(BaseModel):
    advisory_type: str
    title: str
    message: str
    priority: str = "medium"
    status: str = "active"
    valid_until: datetime | None = None


class CropAdvisoryCreate(CropAdvisoryBase):
    farm_id: int
    crop_id: int


class CropAdvisoryUpdate(BaseModel):
    advisory_type: str | None = None
    title: str | None = None
    message: str | None = None
    priority: str | None = None
    status: str | None = None
    valid_until: datetime | None = None


class CropAdvisoryResponse(CropAdvisoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    farm_id: int
    crop_id: int
    created_at: datetime
    updated_at: datetime