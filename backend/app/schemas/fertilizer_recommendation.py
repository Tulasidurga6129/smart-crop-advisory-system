from pydantic import BaseModel, Field


class FertilizerRecommendationRequest(BaseModel):
    temperature: float
    humidity: float = Field(ge=0, le=100)
    moisture: float = Field(ge=0, le=100)
    soil_type: str
    crop_type: str
    nitrogen: float = Field(ge=0)
    potassium: float = Field(ge=0)
    phosphorus: float = Field(ge=0)


class FertilizerRecommendationResponse(BaseModel):
    recommended_fertilizer: str