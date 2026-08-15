from pydantic import BaseModel, Field


class YieldPredictionRequest(BaseModel):
    crop: str = Field(..., min_length=1)
    crop_year: int = Field(..., ge=1900)
    season: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)

    area: float = Field(..., gt=0)
    annual_rainfall: float = Field(..., ge=0)
    fertilizer: float = Field(..., ge=0)
    pesticide: float = Field(..., ge=0)

    avg_temperature: float
    max_temperature: float
    min_temperature: float


class YieldPredictionResponse(BaseModel):
    predicted_yield: float