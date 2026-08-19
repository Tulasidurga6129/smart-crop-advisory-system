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


# Load model once when application starts
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


def generate_explanation(
    crop: str,
    condition: FarmCondition,
    weather: Weather,
) -> str:

    explanations = []

    # Soil pH
    if condition.soil_ph is not None:
        if 6.0 <= condition.soil_ph <= 7.5:
            explanations.append(
                f"soil pH ({condition.soil_ph:.1f}) is within a favorable range"
            )
        else:
            explanations.append(
                f"soil pH is {condition.soil_ph:.1f}"
            )

    # Nitrogen
    if condition.nitrogen is not None:
        if condition.nitrogen >= 40:
            explanations.append(
                f"nitrogen level ({condition.nitrogen:.1f}) is adequate"
            )
        else:
            explanations.append(
                f"nitrogen level is relatively low ({condition.nitrogen:.1f})"
            )

    # Phosphorus
    if condition.phosphorus is not None:
        if condition.phosphorus >= 20:
            explanations.append(
                f"phosphorus level ({condition.phosphorus:.1f}) is adequate"
            )
        else:
            explanations.append(
                f"phosphorus level is relatively low ({condition.phosphorus:.1f})"
            )

    # Potassium
    if condition.potassium is not None:
        if condition.potassium >= 40:
            explanations.append(
                f"potassium level ({condition.potassium:.1f}) is adequate"
            )
        else:
            explanations.append(
                f"potassium level is relatively low ({condition.potassium:.1f})"
            )

    # Temperature
    if weather.temperature is not None:
        explanations.append(
            f"temperature is {weather.temperature:.1f}°C"
        )

    # Humidity
    if weather.humidity is not None:
        explanations.append(
            f"humidity is {weather.humidity:.1f}%"
        )

    # Rainfall
    if weather.rainfall is not None:
        explanations.append(
            f"rainfall is {weather.rainfall:.1f} mm"
        )

    if not explanations:
        return (
            f"{crop.title()} is recommended based on the "
            "available farm conditions."
        )

    return (
        f"{crop.title()} is recommended based on the current "
        "soil and weather conditions: "
        + ", ".join(explanations)
        + "."
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

    # Get latest soil report
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

    # Get latest weather
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

    # Required model inputs
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

    # Prepare input in the exact order used during training
    input_data = [[
        condition.nitrogen,
        condition.phosphorus,
        condition.potassium,
        weather.temperature,
        weather.humidity,
        condition.soil_ph,
        weather.rainfall,
    ]]

    # Get probability for every crop
    probabilities = model.predict_proba(
        input_data
    )[0]

    classes = model.classes_

    # Combine crop names and probabilities
    crop_probabilities = list(
        zip(
            classes,
            probabilities,
        )
    )

    # Sort highest probability first
    crop_probabilities.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    # Select top 3
    top_three = crop_probabilities[:3]

    recommendations = []

    for crop, probability in top_three:

        confidence = round(
            float(probability) * 100,
            2,
        )

        explanation = generate_explanation(
            str(crop),
            condition,
            weather,
        )

        recommendations.append(
            {
                "crop": str(crop),
                "confidence": confidence,
                "explanation": explanation,
            }
        )

    return {
        "farm_id": farm_id,
        "recommendations": recommendations,
    }