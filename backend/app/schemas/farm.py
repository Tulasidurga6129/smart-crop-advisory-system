from pydantic import BaseModel, Field


class FarmCreate(BaseModel):
    farm_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    location: str | None = Field(
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

    land_area: float = Field(
        ...,
        gt=0,
    )

    land_unit: str = Field(
        default="acres",
        max_length=20,
    )

    soil_type: str | None = Field(
        default=None,
        max_length=100,
    )

    irrigation_type: str | None = Field(
        default=None,
        max_length=100,
    )

    current_crop: str | None = Field(
        default=None,
        max_length=100,
    )


class FarmUpdate(BaseModel):
    farm_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    location: str | None = Field(
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

    soil_type: str | None = Field(
        default=None,
        max_length=100,
    )

    irrigation_type: str | None = Field(
        default=None,
        max_length=100,
    )

    current_crop: str | None = Field(
        default=None,
        max_length=100,
    )


class FarmResponse(BaseModel):
    id: int
    farmer_profile_id: int
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

    model_config = {
        "from_attributes": True
    }