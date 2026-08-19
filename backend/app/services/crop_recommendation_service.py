from pathlib import Path

import joblib
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.farm_condition import FarmCondition
from app.models.weather import Weather


# Project root:
# smart-crop-advisory-system/
BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    BASE_DIR
    / "ml"
    / "crop_recommendation"
    / "models"
    / "crop_model.pkl"
)


# Load the model once when the application starts/imports this service.
try:
    model = joblib.load(MODEL_PATH)
except Exception as exc:
    model = None
    MODEL_LOAD_ERROR = str(exc)
else:
    MODEL_LOAD_ERROR = None


def get_latest_condition(
    db: Session,
    farm_id: int,
) -> FarmCondition | None:
    return (
        db.query(FarmCondition)
        .filter(
            FarmCondition.farm_id == farm_id
        )
        .order_by(
            FarmCondition.recorded_at.desc()
        )
        .first()
    )


def get_latest_weather(
    db: Session,
    farm_id: int,
) -> Weather | None:
    return (
        db.query(Weather)
        .filter(
            Weather.farm_id == farm_id
        )
        .order_by(
            Weather.observed_at.desc()
        )
        .first()
    )


def predict_crop(
    db: Session,
    farm_id: int,
) -> dict:

    if model is None:
        raise HTTPException(
            status_code=500,
            detail=(
                "Crop recommendation model could not be loaded. "
                f"{MODEL_LOAD_ERROR}"
            ),
        )

    condition = get_latest_condition(
        db,
        farm_id,
    )

    if not condition:
        raise HTTPException(
            status_code=400,
            detail=(
                "Farm condition data is required before "
                "generating a crop recommendation."
            ),
        )

    weather = get_latest_weather(
        db,
        farm_id,
    )

    if not weather:
        raise HTTPException(
            status_code=400,
            detail=(
                "Weather data is required before "
                "generating a crop recommendation."
            ),
        )

    required_values = {
        "nitrogen": condition.nitrogen,
        "phosphorus": condition.phosphorus,
        "potassium": condition.potassium,
        "soil_ph": condition.soil_ph,
        "temperature": weather.temperature,
        "humidity": weather.humidity,
        "rainfall": weather.rainfall,
    }

    missing_values = [
        name
        for name, value in required_values.items()
        if value is None
    ]

    if missing_values:
        raise HTTPException(
            status_code=400,
            detail=(
                "Missing data required for crop recommendation: "
                + ", ".join(missing_values)
            ),
        )

    input_data = [[
        condition.nitrogen,
        condition.phosphorus,
        condition.potassium,
        weather.temperature,
        weather.humidity,
        condition.soil_ph,
        weather.rainfall,
    ]]

    prediction = model.predict(
        input_data
    )

    recommended_crop = str(
        prediction[0]
    )

    return {
        "farm_id": farm_id,
        "recommended_crop": recommended_crop,
    }