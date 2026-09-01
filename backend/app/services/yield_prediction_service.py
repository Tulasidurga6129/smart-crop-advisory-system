from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.farm import Farm
from app.services.weather_provider_service import (
    get_coordinates_for_farm,
    get_historical_weather_summary,
)

import os
import sys


# --------------------------------------------------
# ML module path
# --------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
    )
)

ML_PATH = os.path.join(
    PROJECT_ROOT,
    "ml",
    "yield_prediction",
)

if ML_PATH not in sys.path:
    sys.path.insert(0, ML_PATH)


from yield_predictor import predict_yield


# --------------------------------------------------
# Existing direct prediction service
# --------------------------------------------------

def predict_crop_yield(
    crop: str,
    crop_year: int,
    season: str,
    state: str,
    area: float,
    annual_rainfall: float,
    avg_temperature: float,
    max_temperature: float,
    min_temperature: float,
) -> float:

    return predict_yield(
        crop=crop,
        crop_year=crop_year,
        season=season,
        state=state,
        area=area,
        annual_rainfall=annual_rainfall,
        avg_temperature=avg_temperature,
        max_temperature=max_temperature,
        min_temperature=min_temperature,
    )

# --------------------------------------------------
# Integrated crop yield prediction
# --------------------------------------------------

def predict_yield_for_crop(
    db: Session,
    crop_id: int,
) -> dict:

    # ----------------------------------------------
    # Get selected crop
    # ----------------------------------------------

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

    # ----------------------------------------------
    # Get farm
    # ----------------------------------------------

    farm = (
        db.query(Farm)
        .filter(Farm.id == crop.farm_id)
        .first()
    )

    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found",
        )

    # ----------------------------------------------
    # Validate crop information
    # ----------------------------------------------

    if not crop.sowing_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Sowing date is required for "
                "yield prediction"
            ),
        )

    if not crop.season:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Crop season is required for "
                "yield prediction"
            ),
        )

    # ----------------------------------------------
    # Validate farm information
    # ----------------------------------------------

    if not farm.state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Farm state is required for "
                "yield prediction"
            ),
        )

    # ----------------------------------------------
    # Determine crop area
    # ----------------------------------------------

    area = crop.area

    if area is None:
        area = farm.land_area

    if area is None or area <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Valid crop area or farm land area "
                "is required for yield prediction"
            ),
        )

    # ----------------------------------------------
    # Crop year
    # ----------------------------------------------

    crop_year = crop.sowing_date.year

    # ----------------------------------------------
    # Get farm coordinates
    # ----------------------------------------------

    try:
        latitude, longitude = get_coordinates_for_farm(
            farm
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "Unable to determine farm coordinates"
            ),
        )

    # ----------------------------------------------
    # Get historical weather
    # ----------------------------------------------

    # Use a completed calendar year for historical weather.
    # If the crop year is the current year, use the previous year.
    current_year = date.today().year

    weather_year = crop_year

    if crop_year >= current_year:
        weather_year = current_year - 1

    start_date = date(
        weather_year,
        1,
        1,
    ).isoformat()

    end_date = date(
        weather_year,
        12,
        31,
    ).isoformat()

    try:
        weather = get_historical_weather_summary(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "Unable to fetch historical "
                "weather data"
            ),
        )

    # ----------------------------------------------
    # Predict yield
    # ----------------------------------------------

    predicted_yield = predict_yield(
        crop=crop.name,
        crop_year=crop_year,
        season=crop.season,
        state=farm.state,
        area=area,
        annual_rainfall=weather["annual_rainfall"],
        avg_temperature=weather["avg_temperature"],
        max_temperature=weather["max_temperature"],
        min_temperature=weather["min_temperature"],
    )

    return {
        "crop_id": crop.id,
        "farm_id": farm.id,
        "crop": crop.name,
        "crop_year": crop_year,
        "weather_year": crop_year,
        "season": crop.season,
        "state": farm.state,
        "area": area,
        "annual_rainfall": weather["annual_rainfall"],
        "avg_temperature": weather["avg_temperature"],
        "max_temperature": weather["max_temperature"],
        "min_temperature": weather["min_temperature"],
        "predicted_yield": predicted_yield,
    }