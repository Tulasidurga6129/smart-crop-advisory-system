from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.farm import Farm
from app.models.farm_condition import FarmCondition
from app.models.weather import Weather
from app.models.crop_advisory import CropAdvisory


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

    condition = get_latest_condition(
        db,
        farm.id,
    )

    weather = get_latest_weather(
        db,
        farm.id,
    )

    # -------------------------------------------------
    # 1. Soil moisture / irrigation recommendation
    # -------------------------------------------------

    if condition and condition.soil_moisture is not None:

        if condition.soil_moisture < 30:
            recommendations.append(
                {
                    "advisory_type": "irrigation",
                    "title": "Low Soil Moisture Detected",
                    "message": (
                        f"Soil moisture is currently "
                        f"{condition.soil_moisture:.1f}%. "
                        f"Irrigation is recommended to reduce "
                        f"water stress for {crop.name}."
                    ),
                    "priority": "high",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=1)
                    ),
                }
            )

        elif condition.soil_moisture < 50:
            recommendations.append(
                {
                    "advisory_type": "irrigation",
                    "title": "Moderate Soil Moisture",
                    "message": (
                        f"Soil moisture is "
                        f"{condition.soil_moisture:.1f}%. "
                        f"Monitor the field and consider "
                        f"irrigation if moisture continues "
                        f"to decline."
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
    # 2. Temperature recommendation
    # -------------------------------------------------

    temperature = None

    if weather and weather.temperature is not None:
        temperature = weather.temperature
    elif condition and condition.temperature is not None:
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

    if weather and weather.rainfall is not None:
        rainfall = weather.rainfall
    elif condition and condition.rainfall is not None:
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

    if condition and condition.soil_ph is not None:

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

    if weather and weather.humidity is not None:
        humidity = weather.humidity
    elif condition and condition.humidity is not None:
        humidity = condition.humidity

    if humidity is not None and humidity >= 85:
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

        # Nitrogen deficiency
        if nitrogen is not None and nitrogen < 40:
            recommendations.append(
                {
                    "advisory_type": "fertilizer",
                    "title": "Low Nitrogen Level Detected",
                    "message": (
                        f"Soil nitrogen level is "
                        f"{nitrogen:.1f}. The level is below "
                        f"the recommended prototype threshold. "
                        f"Consider a nitrogen-rich fertilizer "
                        f"and confirm the requirement through "
                        f"soil testing before application."
                    ),
                    "priority": "high",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=7)
                    ),
                }
            )

        # Phosphorus deficiency
        if phosphorus is not None and phosphorus < 20:
            recommendations.append(
                {
                    "advisory_type": "fertilizer",
                    "title": "Low Phosphorus Level Detected",
                    "message": (
                        f"Soil phosphorus level is "
                        f"{phosphorus:.1f}. The level is below "
                        f"the recommended prototype threshold. "
                        f"Consider a phosphorus-containing "
                        f"fertilizer after confirming the "
                        f"requirement through soil testing."
                    ),
                    "priority": "medium",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=7)
                    ),
                }
            )

        # Potassium deficiency
        if potassium is not None and potassium < 40:
            recommendations.append(
                {
                    "advisory_type": "fertilizer",
                    "title": "Low Potassium Level Detected",
                    "message": (
                        f"Soil potassium level is "
                        f"{potassium:.1f}. The level is below "
                        f"the recommended prototype threshold. "
                        f"Consider a potassium-containing "
                        f"fertilizer after confirming the "
                        f"requirement through soil testing."
                    ),
                    "priority": "high",
                    "status": "active",
                    "valid_until": (
                        datetime.utcnow()
                        + timedelta(days=7)
                    ),
                }
            )

        # Balanced nutrient status
        if (
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
                        f"{crop.name} appear adequate based on "
                        f"the prototype thresholds "
                        f"(N: {nitrogen:.1f}, "
                        f"P: {phosphorus:.1f}, "
                        f"K: {potassium:.1f}). "
                        f"Avoid unnecessary fertilizer "
                        f"application and continue monitoring."
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
    # 6. Crop-weather contextual recommendation
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

    return advisories
