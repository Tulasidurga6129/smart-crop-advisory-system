from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.farmer_profile import FarmerProfile
from app.models.farm import Farm
from app.models.user import User
from app.schemas.farm import (
    FarmCreate,
    FarmResponse,
    FarmUpdate,
)
from app.services.farm_service import (
    create_farm,
    delete_farm,
    get_farm_by_id,
    get_farms_by_profile_id,
    update_farm,
)


router = APIRouter(
    prefix="/farms",
    tags=["Farms"],
)


def get_my_farmer_profile(
    db: Session,
    current_user: User,
) -> FarmerProfile:
    profile = (
        db.query(FarmerProfile)
        .filter(
            FarmerProfile.user_id == current_user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer profile not found",
        )

    return profile


@router.post(
    "",
    response_model=FarmResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_my_farm(
    farm_data: FarmCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = get_my_farmer_profile(
        db,
        current_user,
    )

    return create_farm(
        db,
        profile.id,
        farm_data,
    )


@router.get(
    "",
    response_model=list[FarmResponse],
)
def get_my_farms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = get_my_farmer_profile(
        db,
        current_user,
    )

    return get_farms_by_profile_id(
        db,
        profile.id,
    )


@router.get(
    "/{farm_id}",
    response_model=FarmResponse,
)
def get_my_farm(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = get_my_farmer_profile(
        db,
        current_user,
    )

    farm = get_farm_by_id(
        db,
        farm_id,
    )

    if (
        not farm
        or farm.farmer_profile_id != profile.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found",
        )

    return farm


@router.put(
    "/{farm_id}",
    response_model=FarmResponse,
)
def update_my_farm(
    farm_id: int,
    farm_data: FarmUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = get_my_farmer_profile(
        db,
        current_user,
    )

    farm = get_farm_by_id(
        db,
        farm_id,
    )

    if (
        not farm
        or farm.farmer_profile_id != profile.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found",
        )

    return update_farm(
        db,
        farm,
        farm_data,
    )


@router.delete(
    "/{farm_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_farm(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = get_my_farmer_profile(
        db,
        current_user,
    )

    farm = get_farm_by_id(
        db,
        farm_id,
    )

    if (
        not farm
        or farm.farmer_profile_id != profile.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found",
        )

    delete_farm(
        db,
        farm,
    )

    return None