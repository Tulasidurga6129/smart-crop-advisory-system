from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.crop import Crop
from app.models.farm import Farm
from app.models.farm_condition import FarmCondition
from app.models.weather import Weather
from app.models.user import User
from app.schemas.fertilizer_recommendation import (
    FertilizerRecommendationResponse,
)
from ml.fertilizer_recommendation.fertilizer_predictor import (
    predict_fertilizer,
)
from app.services.weather_service import fetch_and_save_weather

router = APIRouter(
    prefix="/fertilizer-recommendation",
    tags=["Fertilizer Recommendation"],
)


def get_my_crop(
    db: Session,
    current_user: User,
    crop_id: int,
) -> Crop:

    crop = (
        db.query(Crop)
        .filter(Crop.id == crop_id)
        .first()
    )

    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found",
        )

    farm = (
        db.query(Farm)
        .join(Farm.farmer_profile)
        .filter(
            Farm.id == crop.farm_id,
            Farm.farmer_profile.has(
                user_id=current_user.id
            ),
        )
        .first()
    )

    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found",
        )

    return crop


@router.post(
    "/{crop_id}",
    response_model=FertilizerRecommendationResponse,
)
def recommend_fertilizer(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    crop = get_my_crop(
        db,
        current_user,
        crop_id,
    )

    # Get latest soil/farm condition.
    condition = (
        db.query(FarmCondition)
        .filter(
            FarmCondition.farm_id == crop.farm_id
        )
        .order_by(
            FarmCondition.recorded_at.desc()
        )
        .first()
    )

    if not condition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No farm condition found for this farm",
        )

    # Get latest automatically fetched weather.
    weather = (
        db.query(Weather)
        .filter(
            Weather.farm_id == crop.farm_id
        )
        .order_by(
            Weather.observed_at.desc()
        )
        .first()
    )

# If no weather exists, fetch it automatically.
    if not weather:
        farm = (
            db.query(Farm)
            .filter(
                Farm.id == crop.farm_id
            )
            .first()
        )

        if not farm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farm not found",
            )

    try:
        weather = fetch_and_save_weather(
            db,
            farm,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to fetch weather data",
        )

        # Soil/farm-condition values.
    required_condition_fields = {
        "soil_moisture": condition.soil_moisture,
        "soil_type": condition.soil_type,
        "nitrogen": condition.nitrogen,
        "potassium": condition.potassium,
        "phosphorus": condition.phosphorus,
    }

    missing_condition_fields = [
        field
        for field, value in required_condition_fields.items()
        if value is None
    ]

    if missing_condition_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Missing required farm condition fields: "
                + ", ".join(missing_condition_fields)
            ),
        )

    # Automatically fetched weather values.
    required_weather_fields = {
        "temperature": weather.temperature,
        "humidity": weather.humidity,
    }

    missing_weather_fields = [
        field
        for field, value in required_weather_fields.items()
        if value is None
    ]

    if missing_weather_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Missing required weather fields: "
                + ", ".join(missing_weather_fields)
            ),
        )

    fertilizer = predict_fertilizer(
        temperature=weather.temperature,
        humidity=weather.humidity,
        moisture=condition.soil_moisture,
        soil_type=condition.soil_type,
        crop_type=crop.name,
        nitrogen=condition.nitrogen,
        potassium=condition.potassium,
        phosphorus=condition.phosphorus,
    )

    return {
        "recommended_fertilizer": str(fertilizer),
    }