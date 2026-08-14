from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.farm import Farm
from app.schemas.farm import FarmCreate, FarmUpdate


def get_farm_by_id(
    db: Session,
    farm_id: int,
) -> Farm | None:
    statement = select(Farm).where(
        Farm.id == farm_id
    )

    return db.scalar(statement)


def get_farms_by_profile_id(
    db: Session,
    farmer_profile_id: int,
) -> list[Farm]:
    statement = (
        select(Farm)
        .where(
            Farm.farmer_profile_id == farmer_profile_id
        )
        .order_by(Farm.id)
    )

    return list(db.scalars(statement).all())


def create_farm(
    db: Session,
    farmer_profile_id: int,
    farm_data: FarmCreate,
) -> Farm:
    farm = Farm(
        farmer_profile_id=farmer_profile_id,
        **farm_data.model_dump(),
    )

    db.add(farm)
    db.commit()
    db.refresh(farm)

    return farm


def update_farm(
    db: Session,
    farm: Farm,
    farm_data: FarmUpdate,
) -> Farm:
    update_data = farm_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(farm, field, value)

    db.commit()
    db.refresh(farm)

    return farm


def delete_farm(
    db: Session,
    farm: Farm,
) -> None:
    db.delete(farm)
    db.commit()