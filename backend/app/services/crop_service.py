from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.farm import Farm
from app.schemas.crop import CropCreate, CropUpdate



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
    """
    Select a crop for the farm.

    The farmer may select any valid crop.
    AI recommendations are advisory only and do not
    restrict the farmer's choice.
    """

    selected_crop = crop_name.strip()

    # Basic validation
    if not selected_crop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Crop name cannot be empty.",
        )

    # Prevent duplicate planned/active crop selection
    existing_crop = (
        db.query(Crop)
        .filter(
            Crop.farm_id == farm.id,
            Crop.name.ilike(selected_crop),
            Crop.status.in_(["planned", "active"]),
        )
        .first()
    )

    if existing_crop:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Crop '{selected_crop}' is already selected "
                "for this farm."
            ),
        )

    # Create the actual farm crop
    crop = Crop(
        farm_id=farm.id,
        name=selected_crop,
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