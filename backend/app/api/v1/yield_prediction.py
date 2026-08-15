from fastapi import APIRouter

from app.schemas.yield_prediction import (
    YieldPredictionRequest,
    YieldPredictionResponse,
)
from app.services.yield_prediction_service import (
    predict_crop_yield,
)


router = APIRouter(
    prefix="/yield-prediction",
    tags=["Yield Prediction"],
)


@router.post(
    "/predict",
    response_model=YieldPredictionResponse,
)
def predict_yield(
    request: YieldPredictionRequest,
):
    predicted_yield = predict_crop_yield(
        crop=request.crop,
        crop_year=request.crop_year,
        season=request.season,
        state=request.state,
        area=request.area,
        annual_rainfall=request.annual_rainfall,
        fertilizer=request.fertilizer,
        pesticide=request.pesticide,
        avg_temperature=request.avg_temperature,
        max_temperature=request.max_temperature,
        min_temperature=request.min_temperature,
    )

    return YieldPredictionResponse(
        predicted_yield=predicted_yield
    )