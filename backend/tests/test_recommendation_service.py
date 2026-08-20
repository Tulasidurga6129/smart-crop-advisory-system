from datetime import date, timedelta
from unittest.mock import patch
from types import SimpleNamespace

from app.models.crop import Crop
from app.models.farm import Farm
from app.services.recommendation_service import (
    generate_recommendations,
)
from app.models.farm_condition import FarmCondition
from app.models.weather import Weather

def test_generate_recommendations_includes_crop_stage():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    farm = Farm(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=None,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    stage_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation["advisory_type"] == "crop_stage"
    ]

    assert len(stage_recommendations) == 1
    assert stage_recommendations[0]["title"] == "Seedling Stage"
def test_generate_recommendations_skips_crop_stage_when_not_started():
    crop = Crop(
        name="rice",
        sowing_date=date.today() + timedelta(days=10),
    )

    farm = Farm(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=None,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    stage_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation["advisory_type"] == "crop_stage"
    ]

    assert stage_recommendations == []
def test_generate_recommendations_skips_crop_stage_for_unsupported_crop():
    crop = Crop(
        name="dragonfruit",
        sowing_date=date.today() - timedelta(days=30),
    )

    farm = Farm(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=None,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    stage_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation["advisory_type"] == "crop_stage"
    ]

    assert stage_recommendations == []
def test_generate_recommendations_includes_correct_growth_stage():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=70),
    )

    farm = Farm(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=None,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    stage_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation["advisory_type"] == "crop_stage"
    ]

    assert len(stage_recommendations) == 1
    assert stage_recommendations[0]["title"] == "Vegetative Stage"
def test_generate_recommendations_includes_irrigation_for_low_soil_moisture():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    farm = Farm(id=1)

    condition = FarmCondition(
        farm_id=1,
        soil_moisture=20,
    )

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=condition,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    irrigation_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation["advisory_type"] == "irrigation"
    ]

    assert len(irrigation_recommendations) == 1
    assert irrigation_recommendations[0]["priority"] == "high"
    assert irrigation_recommendations[0]["title"] == (
        "Low Soil Moisture Detected"
    )
def test_generate_recommendations_includes_high_temperature_alert():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    farm = Farm(id=1)

    weather = Weather(
        farm_id=1,
        temperature=38,
    )

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=None,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=weather,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    weather_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"] == "High Temperature Alert"
    ]

    assert len(weather_recommendations) == 1
    assert weather_recommendations[0]["priority"] == "high"
def test_generate_recommendations_includes_heavy_rainfall_alert():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    farm = Farm(id=1)

    weather = Weather(
        farm_id=1,
        rainfall=100,
    )

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=None,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=weather,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    rainfall_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"] == "Heavy Rainfall Alert"
    ]

    assert len(rainfall_recommendations) == 1
    assert rainfall_recommendations[0]["priority"] == "high"
def test_generate_recommendations_includes_acidic_soil_alert():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    farm = Farm(id=1)

    condition = FarmCondition(
        farm_id=1,
        soil_ph=5.0,
    )

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=condition,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    soil_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"] == "Acidic Soil Detected"
    ]

    assert len(soil_recommendations) == 1
    assert soil_recommendations[0]["priority"] == "medium"
def test_generate_recommendations_includes_alkaline_soil_alert():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    condition = SimpleNamespace(
        soil_moisture=None,
        temperature=None,
        rainfall=None,
        soil_ph=8.5,
        humidity=None,
        nitrogen=None,
        phosphorus=None,
        potassium=None,
    )

    farm = SimpleNamespace(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=condition,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    alkaline_alerts = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"] == "Alkaline Soil Detected"
    ]

    assert len(alkaline_alerts) == 1
    assert alkaline_alerts[0]["advisory_type"] == "soil"
    assert alkaline_alerts[0]["priority"] == "medium"
def test_generate_recommendations_includes_high_humidity_alert():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    condition = SimpleNamespace(
        soil_moisture=None,
        temperature=None,
        rainfall=None,
        soil_ph=None,
        humidity=90,
        nitrogen=None,
        phosphorus=None,
        potassium=None,
    )

    farm = SimpleNamespace(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=condition,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    humidity_alerts = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"] == "High Humidity Alert"
    ]

    assert len(humidity_alerts) == 1
    assert humidity_alerts[0]["advisory_type"] == "weather"
    assert humidity_alerts[0]["priority"] == "medium"
def test_generate_recommendations_includes_nitrogen_fertilizer_recommendation():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    condition = SimpleNamespace(
        soil_moisture=None,
        temperature=None,
        rainfall=None,
        soil_ph=None,
        humidity=None,
        nitrogen=30,
        phosphorus=30,
        potassium=50,
    )

    farm = SimpleNamespace(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=condition,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    nitrogen_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"] == "Nitrogen Fertilizer Recommended"
    ]

    assert len(nitrogen_recommendations) == 1
    assert nitrogen_recommendations[0]["advisory_type"] == "fertilizer"
    assert nitrogen_recommendations[0]["priority"] == "high"
def test_generate_recommendations_includes_phosphorus_fertilizer_recommendation():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    condition = SimpleNamespace(
        soil_moisture=None,
        temperature=None,
        rainfall=None,
        soil_ph=None,
        humidity=None,
        nitrogen=50,
        phosphorus=10,
        potassium=50,
    )

    farm = SimpleNamespace(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=condition,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    phosphorus_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"] == "Phosphorus Fertilizer Recommended"
    ]

    assert len(phosphorus_recommendations) == 1
    assert phosphorus_recommendations[0]["advisory_type"] == "fertilizer"
    assert phosphorus_recommendations[0]["priority"] == "medium"
def test_generate_recommendations_includes_potassium_fertilizer_recommendation():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    condition = SimpleNamespace(
        soil_moisture=None,
        temperature=None,
        rainfall=None,
        soil_ph=None,
        humidity=None,
        nitrogen=50,
        phosphorus=30,
        potassium=25,
    )

    farm = SimpleNamespace(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=condition,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    potassium_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"] == "Potassium Fertilizer Recommended"
    ]

    assert len(potassium_recommendations) == 1
    assert potassium_recommendations[0]["advisory_type"] == "fertilizer"
    assert potassium_recommendations[0]["priority"] == "high"
def test_generate_recommendations_includes_multiple_nutrient_deficiencies():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    condition = SimpleNamespace(
        soil_moisture=None,
        temperature=None,
        rainfall=None,
        soil_ph=None,
        humidity=None,
        nitrogen=20,
        phosphorus=10,
        potassium=25,
    )

    farm = SimpleNamespace(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=condition,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    multiple_deficiency = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"]
        == "Multiple Nutrient Deficiencies Detected"
    ]

    assert len(multiple_deficiency) == 1
    assert multiple_deficiency[0]["advisory_type"] == "fertilizer"
    assert multiple_deficiency[0]["priority"] == "high"
    assert "nitrogen" in multiple_deficiency[0]["message"]
    assert "phosphorus" in multiple_deficiency[0]["message"]
    assert "potassium" in multiple_deficiency[0]["message"]
def test_generate_recommendations_includes_adequate_nutrient_message():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    condition = SimpleNamespace(
        soil_moisture=None,
        temperature=None,
        rainfall=None,
        soil_ph=None,
        humidity=None,
        nitrogen=50,
        phosphorus=30,
        potassium=50,
    )

    farm = SimpleNamespace(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=condition,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    adequate = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"]
        == "Nutrient Levels Are Adequate"
    ]

    assert len(adequate) == 1
    assert adequate[0]["advisory_type"] == "fertilizer"
    assert adequate[0]["priority"] == "low"
def test_generate_recommendations_includes_favorable_rice_weather():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    weather = SimpleNamespace(
        temperature=28,
        humidity=70,
        rainfall=10,
    )

    farm = SimpleNamespace(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=None,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=weather,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    favorable = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"]
        == "Favorable Weather for Rice"
    ]

    assert len(favorable) == 1
    assert favorable[0]["advisory_type"] == "crop"
    assert favorable[0]["priority"] == "low"
def test_generate_recommendations_includes_moderate_soil_moisture():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    condition = SimpleNamespace(
        soil_moisture=40,
        temperature=None,
        rainfall=None,
        soil_ph=None,
        humidity=None,
        nitrogen=None,
        phosphorus=None,
        potassium=None,
    )

    farm = SimpleNamespace(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=condition,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    moderate = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"] == "Moderate Soil Moisture"
    ]

    assert len(moderate) == 1
    assert moderate[0]["advisory_type"] == "irrigation"
    assert moderate[0]["priority"] == "medium"
def test_generate_recommendations_includes_low_temperature_alert():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    weather = SimpleNamespace(
        temperature=10,
        humidity=None,
        rainfall=None,
    )

    farm = SimpleNamespace(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=None,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=weather,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    alerts = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"] == "Low Temperature Alert"
    ]

    assert len(alerts) == 1
    assert alerts[0]["advisory_type"] == "weather"
    assert alerts[0]["priority"] == "medium"
def test_generate_recommendations_includes_recent_rainfall():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    weather = SimpleNamespace(
        temperature=None,
        humidity=None,
        rainfall=10,
    )

    farm = SimpleNamespace(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=None,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=weather,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    rainfall_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"] == "Recent Rainfall Observed"
    ]

    assert len(rainfall_recommendations) == 1
    assert rainfall_recommendations[0]["advisory_type"] == "weather"
    assert rainfall_recommendations[0]["priority"] == "low"
def test_generate_recommendations_does_not_mark_incomplete_nutrients_as_adequate():
    crop = Crop(
        name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    condition = SimpleNamespace(
        soil_moisture=None,
        temperature=None,
        rainfall=None,
        soil_ph=None,
        humidity=None,
        nitrogen=50,
        phosphorus=None,
        potassium=50,
    )

    farm = SimpleNamespace(id=1)

    with patch(
        "app.services.recommendation_service.get_latest_condition",
        return_value=condition,
    ), patch(
        "app.services.recommendation_service.get_latest_weather",
        return_value=None,
    ):
        recommendations = generate_recommendations(
            db=None,
            farm=farm,
            crop=crop,
        )

    adequate = [
        recommendation
        for recommendation in recommendations
        if recommendation["title"] == "Nutrient Levels Are Adequate"
    ]

    assert len(adequate) == 0