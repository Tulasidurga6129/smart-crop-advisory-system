from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.crop_monitoring import CropMonitoring
from app.models.farm import Farm
from app.models.farmer_profile import FarmerProfile
from app.schemas.crop_monitoring import (
    CropMonitoringCreate,
    CropMonitoringUpdate,
)


def get_crop_for_user(
    db: Session,
    crop_id: int,
    user_id: int,
) -> Crop | None:
    return (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .join(
            FarmerProfile,
            Farm.farmer_profile_id == FarmerProfile.id,
        )
        .filter(
            Crop.id == crop_id,
            FarmerProfile.user_id == user_id,
        )
        .first()
    )


def create_monitoring(
    db: Session,
    user_id: int,
    data: CropMonitoringCreate,
) -> CropMonitoring | None:
    crop = get_crop_for_user(
        db=db,
        crop_id=data.crop_id,
        user_id=user_id,
    )

    if not crop:
        return None

    monitoring = CropMonitoring(
        crop_id=data.crop_id,
        monitoring_date=data.monitoring_date,
        growth_stage=data.growth_stage,
        plant_height=data.plant_height,
        crop_health=data.crop_health,
        pest_observed=data.pest_observed,
        disease_observed=data.disease_observed,
        observation_notes=data.observation_notes,
    )

    db.add(monitoring)
    db.commit()
    db.refresh(monitoring)

    return monitoring


def get_monitoring_records(
    db: Session,
    user_id: int,
    crop_id: int,
) -> list[CropMonitoring] | None:
    crop = get_crop_for_user(
        db=db,
        crop_id=crop_id,
        user_id=user_id,
    )

    if not crop:
        return None

    return (
        db.query(CropMonitoring)
        .filter(
            CropMonitoring.crop_id == crop_id,
        )
        .order_by(
            CropMonitoring.monitoring_date.desc(),
            CropMonitoring.id.desc(),
        )
        .all()
    )


def get_monitoring(
    db: Session,
    user_id: int,
    monitoring_id: int,
) -> CropMonitoring | None:
    return (
        db.query(CropMonitoring)
        .join(Crop, CropMonitoring.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .join(
            FarmerProfile,
            Farm.farmer_profile_id == FarmerProfile.id,
        )
        .filter(
            CropMonitoring.id == monitoring_id,
            FarmerProfile.user_id == user_id,
        )
        .first()
    )


def update_monitoring(
    db: Session,
    user_id: int,
    monitoring_id: int,
    data: CropMonitoringUpdate,
) -> CropMonitoring | None:
    monitoring = get_monitoring(
        db=db,
        user_id=user_id,
        monitoring_id=monitoring_id,
    )

    if not monitoring:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(monitoring, field, value)

    db.commit()
    db.refresh(monitoring)

    return monitoring


def delete_monitoring(
    db: Session,
    user_id: int,
    monitoring_id: int,
) -> bool:
    monitoring = get_monitoring(
        db=db,
        user_id=user_id,
        monitoring_id=monitoring_id,
    )

    if not monitoring:
        return False

    db.delete(monitoring)
    db.commit()

    return True