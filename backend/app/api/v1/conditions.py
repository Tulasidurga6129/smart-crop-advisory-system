from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.farm import Farm
from app.models.farm_condition import FarmCondition
from app.models.user import User
from app.schemas.farm_condition import (
    FarmConditionCreate,
    FarmConditionResponse,
    FarmConditionUpdate,
)
from app.services.farm_condition_service import (
    create_condition,
    delete_condition,
    get_condition_by_id,
    get_conditions_by_farm_id,
    update_condition,
)


router = APIRouter(
    prefix="/conditions",
    tags=["Farm Conditions"],
)


def get_my_farm(
    db: Session,
    current_user: User,
    farm_id: int,
) -> Farm:
    farm = (
        db.query(Farm)
        .join(
            Farm.farmer_profile
        )
        .filter(
            Farm.id == farm_id,
            Farm.farmer_profile.has(
                user_id=current_user.id
            ),
        )
        .first()
    )

    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found",
        )

    return farm


@router.post(
    "/farm/{farm_id}",
    response_model=FarmConditionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_my_condition(
    farm_id: int,
    condition_data: FarmConditionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_my_farm(
        db,
        current_user,
        farm_id,
    )

    return create_condition(
        db,
        farm_id,
        condition_data,
    )


@router.get(
    "/farm/{farm_id}",
    response_model=list[FarmConditionResponse],
)
def get_my_farm_conditions(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_my_farm(
        db,
        current_user,
        farm_id,
    )

    return get_conditions_by_farm_id(
        db,
        farm_id,
    )


@router.get(
    "/{condition_id}",
    response_model=FarmConditionResponse,
)
def get_my_condition(
    condition_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    condition = get_condition_by_id(
        db,
        condition_id,
    )

    if not condition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm condition not found",
        )

    get_my_farm(
        db,
        current_user,
        condition.farm_id,
    )

    return condition


@router.put(
    "/{condition_id}",
    response_model=FarmConditionResponse,
)
def update_my_condition(
    condition_id: int,
    condition_data: FarmConditionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    condition = get_condition_by_id(
        db,
        condition_id,
    )

    if not condition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm condition not found",
        )

    get_my_farm(
        db,
        current_user,
        condition.farm_id,
    )

    return update_condition(
        db,
        condition,
        condition_data,
    )


@router.delete(
    "/{condition_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_condition(
    condition_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    condition = get_condition_by_id(
        db,
        condition_id,
    )

    if not condition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm condition not found",
        )

    get_my_farm(
        db,
        current_user,
        condition.farm_id,
    )

    delete_condition(
        db,
        condition,
    )

    return None