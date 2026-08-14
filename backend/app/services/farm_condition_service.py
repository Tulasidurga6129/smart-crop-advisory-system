from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.farm_condition import FarmCondition
from app.schemas.farm_condition import (
    FarmConditionCreate,
    FarmConditionUpdate,
)


def get_condition_by_id(
    db: Session,
    condition_id: int,
) -> FarmCondition | None:
    statement = select(FarmCondition).where(
        FarmCondition.id == condition_id
    )

    return db.scalar(statement)


def get_conditions_by_farm_id(
    db: Session,
    farm_id: int,
) -> list[FarmCondition]:
    statement = (
        select(FarmCondition)
        .where(
            FarmCondition.farm_id == farm_id
        )
        .order_by(FarmCondition.recorded_at.desc())
    )

    return list(db.scalars(statement).all())


def create_condition(
    db: Session,
    farm_id: int,
    condition_data: FarmConditionCreate,
) -> FarmCondition:
    condition = FarmCondition(
        farm_id=farm_id,
        **condition_data.model_dump(),
    )

    db.add(condition)
    db.commit()
    db.refresh(condition)

    return condition


def update_condition(
    db: Session,
    condition: FarmCondition,
    condition_data: FarmConditionUpdate,
) -> FarmCondition:
    update_data = condition_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(condition, field, value)

    db.commit()
    db.refresh(condition)

    return condition


def delete_condition(
    db: Session,
    condition: FarmCondition,
) -> None:
    db.delete(condition)
    db.commit()