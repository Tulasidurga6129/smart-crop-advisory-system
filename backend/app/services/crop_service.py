from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.farm import Farm
from app.schemas.crop import CropCreate, CropUpdate
from app.services.crop_recommendation_service import predict_crop


def get_crop_by_id(
    db: Session,
    crop_id: int,
) -> Crop | None:
    statement = select(Crop).where(
        Crop.id == crop_id
    )

    return db.scalar(statement)


def get_crops_by_farm_id(
    db: Session,
    farm_id: int,
) -> list[Crop]:
    statement = (
        select(Crop)
        .where(
            Crop.farm_id == farm_id
        )
        .order_by(Crop.id)
    )

    return list(db.scalars(statement).all())


def select_recommended_crop(
    db: Session,
    farm: Farm,
    crop_name: str,
    season: str,
    sowing_date=None,
    expected_harvest_date=None,
    variety=None,
    area=None,
) -> Crop:
    # Generate the current top-3 recommendations
    recommendation = predict_crop(
        db=db,
        farm_id=farm.id,
    )

    recommended_crops = {
        item["crop"].strip().lower()
        for item in recommendation["recommendations"]
    }

    selected_crop = crop_name.strip().lower()

    # Farmer can select only one of the recommended crops
    if selected_crop not in recommended_crops:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Crop '{crop_name}' was not among the "
                "top recommended crops for this farm."
            ),
        )

    # Prevent duplicate planned/active crop selection
    existing_crop = (
        db.query(Crop)
        .filter(
            Crop.farm_id == farm.id,
            Crop.name.ilike(crop_name.strip()),
            Crop.status.in_(["planned", "active"]),
        )
        .first()
    )

    if existing_crop:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Crop '{crop_name}' is already selected "
                "for this farm."
            ),
        )

    # Create the actual farm crop
    crop = Crop(
        farm_id=farm.id,
        name=crop_name.strip(),
        variety=variety,
        season=season,
        sowing_date=sowing_date,
        expected_harvest_date=expected_harvest_date,
        area=area,
        status="planned",
    )

    db.add(crop)
    db.commit()
    db.refresh(crop)

    return crop


def create_crop(
    db: Session,
    crop_data: CropCreate,
) -> Crop:
    crop = Crop(
        **crop_data.model_dump(),
    )

    db.add(crop)
    db.commit()
    db.refresh(crop)

    return crop


def update_crop(
    db: Session,
    crop: Crop,
    crop_data: CropUpdate,
) -> Crop:
    update_data = crop_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(crop, field, value)

    db.commit()
    db.refresh(crop)

    return crop


def delete_crop(
    db: Session,
    crop: Crop,
) -> None:
    db.delete(crop)
    db.commit()