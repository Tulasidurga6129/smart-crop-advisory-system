from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.crop_advisory import CropAdvisory
from app.models.farm import Farm
from app.models.farm_condition import FarmCondition
from app.models.weather import Weather


def get_farm_dashboard(
    db: Session,
    farm: Farm,
):
    crops = (
        db.query(Crop)
        .filter(Crop.farm_id == farm.id)
        .order_by(Crop.id)
        .all()
    )

    latest_condition = (
        db.query(FarmCondition)
        .filter(
            FarmCondition.farm_id == farm.id
        )
        .order_by(
            FarmCondition.recorded_at.desc()
        )
        .first()
    )

    latest_weather = (
        db.query(Weather)
        .filter(
            Weather.farm_id == farm.id
        )
        .order_by(
            Weather.observed_at.desc()
        )
        .first()
    )

    active_advisories = (
        db.query(CropAdvisory)
        .filter(
            CropAdvisory.farm_id == farm.id,
            CropAdvisory.status == "active",
        )
        .order_by(
            CropAdvisory.created_at.desc()
        )
        .all()
    )

    high_count = sum(
        1
        for advisory in active_advisories
        if advisory.priority == "high"
    )

    medium_count = sum(
        1
        for advisory in active_advisories
        if advisory.priority == "medium"
    )

    low_count = sum(
        1
        for advisory in active_advisories
        if advisory.priority == "low"
    )

    total_count = len(active_advisories)

    top_priority = None

    if high_count > 0:
        top_priority = "high"
    elif medium_count > 0:
        top_priority = "medium"
    elif low_count > 0:
        top_priority = "low"

    return {
        "farm": farm,
        "crops": crops,
        "latest_condition": latest_condition,
        "latest_weather": latest_weather,
        "active_advisories": active_advisories,
        "summary": {
            "high": high_count,
            "medium": medium_count,
            "low": low_count,
            "total": total_count,
            "top_priority": top_priority,
        },
    }