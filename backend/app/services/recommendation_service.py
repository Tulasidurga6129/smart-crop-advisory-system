from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.farm import Farm
from app.models.farm_condition import FarmCondition
from app.models.weather import Weather
from app.models.crop_advisory import CropAdvisory
from app.services import notification_service
from app.services.crop_lifecycle_service import get_crop_lifecycle
from app.services.weather_service import get_fresh_weather
from app.services.weather_provider_service import (
    get_coordinates_for_farm,
    get_tomorrow_weather_forecast,
)


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


def generate_recommendations(
    db: Session,
    farm: Farm,
    crop: Crop,
) -> list[dict]:

    recommendations = []

    lifecycle = get_crop_lifecycle(
        crop_name=crop.name,
        sowing_date=crop.sowing_date,
        expected_harvest_date=crop.expected_harvest_date,
    )

    # -------------------------------------------------
    # Crop lifecycle recommendation
    # -------------------------------------------------

    if lifecycle["supported"] and lifecycle["growth_stage"] not in (
        None,
        "Not Started",
    ):
        recommendations.append(
            {
                "advisory_type": "crop_stage",
                "title": f"{lifecycle['growth_stage']} Stage",
                "message": (
                    f"{crop.name} is currently in the "
                    f"{lifecycle['growth_stage']} stage. "
                    f"Continue monitoring the crop according "
                    f"to its current growth stage."
                ),
                "priority": "low",
                "status": "active",
                "valid_until": (
                    datetime.utcnow()
                    + timedelta(days=3)
                ),
            }
        )

    # -------------------------------------------------
    # Get latest farm condition
    # -------------------------------------------------

    condition = get_latest_condition(
        db,
        farm.id,
    )

    # -------------------------------------------------
    # Get fresh weather automatically
    # -------------------------------------------------

    try:
        weather = get_fresh_weather(
            db,
            farm,
        )
    except Exception:
        weather = get_latest_weather(
            db,
            farm.id,
        )

    # -------------------------------------------------
    # Get tomorrow's weather forecast automatically
    # -------------------------------------------------

    tomorrow_weather = None

    try:
        latitude, longitude = get_coordinates_for_farm(
            farm
        )

        tomorrow_weather = get_tomorrow_weather_forecast(
            latitude,
            longitude,
        )

    except Exception:
        tomorrow_weather = None

        # -------------------------------------------------
    # 1. Automatic future-weather-aware irrigation
    # -------------------------------------------------

    soil_moisture = None

    if (
        condition
        and condition.soil_moisture is not None
    ):
        soil_moisture = condition.soil_moisture

    # Tomorrow's forecast values
    forecast_rainfall = None
    precipitation_probability = None

    if tomorrow_weather:

        forecast_rainfall = tomorrow_weather.get(
            "rainfall"
        )

        precipitation_probability = (
            tomorrow_weather.get(
                "precipitation_probability"
            )
        )

    # -------------------------------------------------
    # Determine rainfall confidence
    # -------------------------------------------------

    strong_rain_expected = (
        forecast_rainfall is not None
        and precipitation_probability is not None
        and forecast_rainfall >= 10
        and precipitation_probability >= 60
    )

    moderate_rain_expected = (
        forecast_rainfall is not None
        and precipitation_probability is not None
        and forecast_rainfall >= 5
        and precipitation_probability >= 50
    )

    little_rain_expected = (
        forecast_rainfall is not None
        and forecast_rainfall < 5
    )

    # -------------------------------------------------
    # Current crop growth stage
    # -------------------------------------------------

    growth_stage = lifecycle.get(
        "growth_stage"
    )

    stage_text = (
        growth_stage
        if growth_stage
        and growth_stage != "Not Started"
        else "current growth stage"
    )

    # -------------------------------------------------
    # Very dry soil
    # -------------------------------------------------

    if (
        soil_moisture is not None
        and soil_moisture < 30
    ):

        # Strong rainfall is expected
        if strong_rain_expected:

            recommendations.append(
                {
                    "advisory_type": "irrigation",
                    "title": "Irrigation Can Be Delayed",
                    "message": (
                        f"Soil moisture is currently "
                        f"{soil_moisture:.1f}% for {crop.name} "
                        f"during the {stage_text} stage. "
                        f"Approximately "
                        f"{forecast_rainfall:.1f} mm of rainfall "
                        f"is forecast for tomorrow with a "
                        f"{precipitation_probability:.0f}% probability. "
                        f"Irrigation can be delayed to avoid "
                        f"unnecessary water use. Monitor the field "
                        f"and reassess soil moisture after rainfall."
                    ),
                    "priority": "medium",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=1)
                    ),
                }
            )

        # Moderate / uncertain rainfall
        elif moderate_rain_expected:

            recommendations.append(
                {
                    "advisory_type": "irrigation",
                    "title": "Irrigation May Be Needed",
                    "message": (
                        f"Soil moisture is currently "
                        f"{soil_moisture:.1f}% for {crop.name}. "
                        f"About {forecast_rainfall:.1f} mm of rainfall "
                        f"is forecast tomorrow with a "
                        f"{precipitation_probability:.0f}% probability. "
                        f"Rainfall may provide some moisture, but "
                        f"the forecast is not strong enough to rely "
                        f"on completely. Monitor field conditions "
                        f"before irrigating."
                    ),
                    "priority": "medium",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=1)
                    ),
                }
            )

        # Little or no rainfall
        else:

            rainfall_text = (
                f"{forecast_rainfall:.1f} mm"
                if forecast_rainfall is not None
                else "no reliable rainfall amount"
            )

            probability_text = (
                f"{precipitation_probability:.0f}%"
                if precipitation_probability is not None
                else "unavailable"
            )

            recommendations.append(
                {
                    "advisory_type": "irrigation",
                    "title": "Irrigation Recommended",
                    "message": (
                        f"Soil moisture is currently "
                        f"{soil_moisture:.1f}% for {crop.name} "
                        f"during the {stage_text} stage. "
                        f"Only {rainfall_text} of rainfall is "
                        f"forecast for tomorrow with a "
                        f"{probability_text} probability. "
                        f"Rainfall is unlikely to provide enough "
                        f"moisture, so irrigation is recommended "
                        f"to reduce water stress."
                    ),
                    "priority": "high",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=1)
                    ),
                }
            )

    # -------------------------------------------------
    # Moderate soil moisture
    # -------------------------------------------------

    elif (
        soil_moisture is not None
        and soil_moisture < 50
    ):

        # Strong rainfall expected
        if strong_rain_expected:

            recommendations.append(
                {
                    "advisory_type": "irrigation",
                    "title": "Rainfall Expected — Monitor Irrigation",
                    "message": (
                        f"Soil moisture is currently "
                        f"{soil_moisture:.1f}% for {crop.name}. "
                        f"Approximately "
                        f"{forecast_rainfall:.1f} mm of rainfall "
                        f"is forecast tomorrow with a "
                        f"{precipitation_probability:.0f}% probability. "
                        f"Avoid unnecessary irrigation and "
                        f"monitor the field."
                    ),
                    "priority": "low",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=1)
                    ),
                }
            )

        # Moderate rainfall expected
        elif moderate_rain_expected:

            recommendations.append(
                {
                    "advisory_type": "irrigation",
                    "title": "Monitor Irrigation",
                    "message": (
                        f"Soil moisture is currently "
                        f"{soil_moisture:.1f}% for {crop.name}. "
                        f"Approximately "
                        f"{forecast_rainfall:.1f} mm of rainfall "
                        f"is forecast tomorrow with a "
                        f"{precipitation_probability:.0f}% probability. "
                        f"Monitor the field and consider delaying "
                        f"irrigation if rainfall occurs."
                    ),
                    "priority": "low",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=1)
                    ),
                }
            )

        # Little/no rainfall
        else:

            recommendations.append(
                {
                    "advisory_type": "irrigation",
                    "title": "Irrigation May Be Needed",
                    "message": (
                        f"Soil moisture is currently "
                        f"{soil_moisture:.1f}% for {crop.name}. "
                        f"Tomorrow's rainfall forecast is low "
                        f"or uncertain. Monitor soil moisture "
                        f"closely and consider irrigation if "
                        f"moisture continues to decline."
                    ),
                    "priority": "medium",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=1)
                    ),
                }
            )

    # -------------------------------------------------
    # Adequate soil moisture
    # -------------------------------------------------

    elif (
        soil_moisture is not None
        and soil_moisture >= 50
    ):

        recommendations.append(
            {
                "advisory_type": "irrigation",
                "title": "Irrigation Not Currently Required",
                "message": (
                    f"Soil moisture is currently "
                    f"{soil_moisture:.1f}% for {crop.name}. "
                    f"Current soil moisture appears adequate. "
                    f"Continue monitoring the field and avoid "
                    f"unnecessary irrigation."
                ),
                "priority": "low",
                "status": "active",
                "valid_until": (
                    datetime.utcnow()
                    + timedelta(days=1)
                ),
            }
        )

    # -------------------------------------------------
    # No soil moisture data
    # -------------------------------------------------

    else:

        if strong_rain_expected:

            recommendations.append(
                {
                    "advisory_type": "irrigation",
                    "title": "Rainfall Expected",
                    "message": (
                        f"Approximately "
                        f"{forecast_rainfall:.1f} mm of rainfall "
                        f"is forecast tomorrow with a "
                        f"{precipitation_probability:.0f}% probability. "
                        f"Soil moisture data is unavailable, so "
                        f"avoid unnecessary irrigation and "
                        f"monitor field conditions."
                    ),
                    "priority": "low",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=1)
                    ),
                }
            )

        elif forecast_rainfall is not None:

            recommendations.append(
                {
                    "advisory_type": "irrigation",
                    "title": "Irrigation Monitoring Recommended",
                    "message": (
                        f"Approximately "
                        f"{forecast_rainfall:.1f} mm of rainfall "
                        f"is forecast tomorrow. Soil moisture "
                        f"data is unavailable, so inspect field "
                        f"conditions before irrigating "
                        f"{crop.name}."
                    ),
                    "priority": "medium",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=1)
                    ),
                }
            )
    # -------------------------------------------------
    # 2. Temperature recommendation
    # -------------------------------------------------

    temperature = None

    if (
        weather
        and weather.temperature is not None
    ):
        temperature = weather.temperature

    elif (
        condition
        and condition.temperature is not None
    ):
        temperature = condition.temperature

    if temperature is not None:

        if temperature >= 35:
            recommendations.append(
                {
                    "advisory_type": "weather",
                    "title": "High Temperature Alert",
                    "message": (
                        f"Temperature is currently "
                        f"{temperature:.1f}°C. High temperature "
                        f"may cause heat and water stress in "
                        f"{crop.name}. Ensure adequate irrigation "
                        f"and monitor crop condition."
                    ),
                    "priority": "high",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=1)
                    ),
                }
            )

        elif temperature < 15:
            recommendations.append(
                {
                    "advisory_type": "weather",
                    "title": "Low Temperature Alert",
                    "message": (
                        f"Temperature is currently "
                        f"{temperature:.1f}°C. Low temperature "
                        f"may slow crop growth. Monitor "
                        f"{crop.name} for temperature stress."
                    ),
                    "priority": "medium",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=2)
                    ),
                }
            )

    # -------------------------------------------------
    # 3. Heavy rainfall recommendation
    # -------------------------------------------------

    rainfall = None

    if (
        weather
        and weather.rainfall is not None
    ):
        rainfall = weather.rainfall

    elif (
        condition
        and condition.rainfall is not None
    ):
        rainfall = condition.rainfall

    if rainfall is not None:

        if rainfall >= 50:
            recommendations.append(
                {
                    "advisory_type": "weather",
                    "title": "Heavy Rainfall Alert",
                    "message": (
                        f"Rainfall is currently "
                        f"{rainfall:.1f} mm. Heavy rainfall "
                        f"may cause waterlogging and nutrient "
                        f"loss. Check field drainage and avoid "
                        f"unnecessary irrigation."
                    ),
                    "priority": "high",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=1)
                    ),
                }
            )

        elif rainfall > 0:
            recommendations.append(
                {
                    "advisory_type": "weather",
                    "title": "Recent Rainfall Observed",
                    "message": (
                        f"Recent rainfall of "
                        f"{rainfall:.1f} mm has been recorded "
                        f"for the farm. Monitor field conditions "
                        f"and avoid unnecessary irrigation until "
                        f"soil moisture is assessed."
                    ),
                    "priority": "low",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=1)
                    ),
                }
            )

    # -------------------------------------------------
    # 4. Soil pH recommendation
    # -------------------------------------------------

    if (
        condition
        and condition.soil_ph is not None
    ):

        if condition.soil_ph < 5.5:
            recommendations.append(
                {
                    "advisory_type": "soil",
                    "title": "Acidic Soil Detected",
                    "message": (
                        f"Soil pH is "
                        f"{condition.soil_ph:.1f}, indicating "
                        f"acidic soil conditions. Soil amendment "
                        f"may be required. Consider soil testing "
                        f"and suitable corrective measures."
                    ),
                    "priority": "medium",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=7)
                    ),
                }
            )

        elif condition.soil_ph > 8.0:
            recommendations.append(
                {
                    "advisory_type": "soil",
                    "title": "Alkaline Soil Detected",
                    "message": (
                        f"Soil pH is "
                        f"{condition.soil_ph:.1f}, indicating "
                        f"alkaline soil conditions. Consider "
                        f"soil testing and appropriate soil "
                        f"management practices."
                    ),
                    "priority": "medium",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=7)
                    ),
                }
            )

    # -------------------------------------------------
    # 5. High humidity recommendation
    # -------------------------------------------------

    humidity = None

    if (
        weather
        and weather.humidity is not None
    ):
        humidity = weather.humidity

    elif (
        condition
        and condition.humidity is not None
    ):
        humidity = condition.humidity

    if (
        humidity is not None
        and humidity >= 85
    ):
        recommendations.append(
            {
                "advisory_type": "weather",
                "title": "High Humidity Alert",
                "message": (
                    f"Humidity is currently "
                    f"{humidity:.1f}%. High humidity can "
                    f"increase the risk of fungal and other "
                    f"crop-related problems. Monitor the "
                    f"{crop.name} crop closely."
                ),
                "priority": "medium",
                "status": "active",
                "valid_until": (
                    datetime.utcnow()
                    + timedelta(days=2)
                ),
            }
        )

    # -------------------------------------------------
    # 6. Fertilizer / nutrient recommendation
    # -------------------------------------------------

    if condition:

        nitrogen = condition.nitrogen
        phosphorus = condition.phosphorus
        potassium = condition.potassium

        nutrient_deficiencies = []

        # Nitrogen deficiency
        if (
            nitrogen is not None
            and nitrogen < 40
        ):
            nutrient_deficiencies.append(
                "nitrogen"
            )

        # Phosphorus deficiency
        if (
            phosphorus is not None
            and phosphorus < 20
        ):
            nutrient_deficiencies.append(
                "phosphorus"
            )

        # Potassium deficiency
        if (
            potassium is not None
            and potassium < 40
        ):
            nutrient_deficiencies.append(
                "potassium"
            )

        # -------------------------------------------------
        # Multiple nutrient deficiencies
        # -------------------------------------------------

        if len(nutrient_deficiencies) > 1:

            deficiency_names = ", ".join(
                nutrient_deficiencies
            )

            fertilizer_sources = []

            if "nitrogen" in nutrient_deficiencies:
                fertilizer_sources.append(
                    "nitrogen fertilizer such as urea"
                )

            if "phosphorus" in nutrient_deficiencies:
                fertilizer_sources.append(
                    "phosphorus fertilizer such as DAP or SSP"
                )

            if "potassium" in nutrient_deficiencies:
                fertilizer_sources.append(
                    "potassium fertilizer such as MOP"
                )

            fertilizer_text = "; ".join(
                fertilizer_sources
            )

            recommendations.append(
                {
                    "advisory_type": "fertilizer",
                    "title": "Multiple Nutrient Deficiencies Detected",
                    "message": (
                        f"Soil analysis indicates low "
                        f"{deficiency_names} levels for "
                        f"{crop.name}. Consider suitable "
                        f"fertilizer sources such as "
                        f"{fertilizer_text}. "
                        f"Actual fertilizer selection and "
                        f"application rate should be confirmed "
                        f"using crop stage, soil-test results, "
                        f"and local agricultural recommendations."
                    ),
                    "priority": "high",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=7)
                    ),
                }
            )

        # -------------------------------------------------
        # Single nutrient deficiency
        # -------------------------------------------------

        elif len(nutrient_deficiencies) == 1:

            deficiency = nutrient_deficiencies[0]

            if deficiency == "nitrogen":

                recommendations.append(
                    {
                        "advisory_type": "fertilizer",
                        "title": "Nitrogen Fertilizer Recommended",
                        "message": (
                            f"Soil nitrogen level is "
                            f"{nitrogen:.1f}, which is below "
                            f"the prototype threshold. "
                            f"A nitrogen source such as urea "
                            f"may be considered for {crop.name}. "
                            f"Confirm the required application "
                            f"rate using soil-test results, "
                            f"crop stage, and local agricultural "
                            f"recommendations."
                        ),
                        "priority": "high",
                        "status": "active",
                        "valid_until": (
                            datetime.utcnow()
                            + timedelta(days=7)
                        ),
                    }
                )

            elif deficiency == "phosphorus":

                recommendations.append(
                    {
                        "advisory_type": "fertilizer",
                        "title": "Phosphorus Fertilizer Recommended",
                        "message": (
                            f"Soil phosphorus level is "
                            f"{phosphorus:.1f}, which is below "
                            f"the prototype threshold. "
                            f"A phosphorus source such as "
                            f"DAP or SSP may be considered "
                            f"for {crop.name}. Confirm the "
                            f"required application rate using "
                            f"soil-test results, crop stage, "
                            f"and local agricultural "
                            f"recommendations."
                        ),
                        "priority": "medium",
                        "status": "active",
                        "valid_until": (
                            datetime.utcnow()
                            + timedelta(days=7)
                        ),
                    }
                )

            elif deficiency == "potassium":

                recommendations.append(
                    {
                        "advisory_type": "fertilizer",
                        "title": "Potassium Fertilizer Recommended",
                        "message": (
                            f"Soil potassium level is "
                            f"{potassium:.1f}, which is below "
                            f"the prototype threshold. "
                            f"A potassium source such as MOP "
                            f"may be considered for {crop.name}. "
                            f"Confirm the required application "
                            f"rate using soil-test results, "
                            f"crop stage, and local agricultural "
                            f"recommendations."
                        ),
                        "priority": "high",
                        "status": "active",
                        "valid_until": (
                            datetime.utcnow()
                            + timedelta(days=7)
                        ),
                    }
                )

        # -------------------------------------------------
        # All nutrients adequate
        # -------------------------------------------------

        elif (
            nitrogen is not None
            and phosphorus is not None
            and potassium is not None
            and nitrogen >= 40
            and phosphorus >= 20
            and potassium >= 40
        ):

            recommendations.append(
                {
                    "advisory_type": "fertilizer",
                    "title": "Nutrient Levels Are Adequate",
                    "message": (
                        f"Current soil nutrient levels for "
                        f"{crop.name} appear adequate based "
                        f"on the prototype thresholds "
                        f"(N: {nitrogen:.1f}, "
                        f"P: {phosphorus:.1f}, "
                        f"K: {potassium:.1f}). "
                        f"Avoid unnecessary fertilizer "
                        f"application and continue monitoring "
                        f"soil conditions."
                    ),
                    "priority": "low",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=7)
                    ),
                }
            )

    # -------------------------------------------------
    # 7. Crop-weather contextual recommendation
    # -------------------------------------------------

    if (
        crop.name.lower() == "rice"
        and weather
        and temperature is not None
        and humidity is not None
        and rainfall is not None
        and 20 <= temperature <= 35
        and 50 <= humidity <= 85
        and rainfall < 50
    ):
        recommendations.append(
            {
                "advisory_type": "crop",
                "title": "Favorable Weather for Rice",
                "message": (
                    f"Current weather conditions are generally "
                    f"favorable for {crop.name}. Temperature is "
                    f"{temperature:.1f}°C, humidity is "
                    f"{humidity:.1f}%, and recorded rainfall is "
                    f"{rainfall:.1f} mm. Continue regular crop "
                    f"monitoring and follow the planned crop "
                    f"management practices."
                ),
                "priority": "low",
                "status": "active",
                "valid_until": (
                    datetime.utcnow()
                    + timedelta(days=2)
                ),
            }
        )

    return recommendations


def create_recommendations(
    db: Session,
    farm: Farm,
    crop: Crop,
    user_id: int,
) -> list[CropAdvisory]:

    recommendations = generate_recommendations(
        db,
        farm,
        crop,
    )

    advisories = []

    for recommendation in recommendations:

        # Prevent duplicate active advisories
        existing = (
            db.query(CropAdvisory)
            .filter(
                CropAdvisory.farm_id == farm.id,
                CropAdvisory.crop_id == crop.id,
                CropAdvisory.advisory_type
                == recommendation["advisory_type"],
                CropAdvisory.title
                == recommendation["title"],
                CropAdvisory.status == "active",
            )
            .first()
        )

        if existing:
            advisories.append(existing)
            continue

        advisory = CropAdvisory(
            farm_id=farm.id,
            crop_id=crop.id,
            advisory_type=recommendation[
                "advisory_type"
            ],
            title=recommendation["title"],
            message=recommendation["message"],
            priority=recommendation["priority"],
            status=recommendation["status"],
            valid_until=recommendation[
                "valid_until"
            ],
        )

        db.add(advisory)
        advisories.append(advisory)

        db.commit()

    for advisory in advisories:

        db.refresh(advisory)

        notification_service.create_advisory_notification_if_missing(
            db=db,
            user_id=user_id,
            farm_id=advisory.farm_id,
            crop_id=advisory.crop_id,
            notification_type=advisory.advisory_type,
            title=advisory.title,
            message=advisory.message,
            priority=advisory.priority,
        )

    return advisories