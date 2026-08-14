from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.crop import Crop
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