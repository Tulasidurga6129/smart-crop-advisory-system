from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.farmer_profile import (
    FarmerProfileCreate,
    FarmerProfileResponse,
    FarmerProfileUpdate,
)
from app.services.farmer_profile_service import (
    create_profile,
    get_profile_by_user_id,
    update_profile,
)


router = APIRouter(
    prefix="/users/me/profile",
    tags=["Farmer Profile"],
)


@router.post(
    "",
    response_model=FarmerProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_my_profile(
    profile_data: FarmerProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing_profile = get_profile_by_user_id(
        db,
        current_user.id,
    )

    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Farmer profile already exists",
        )

    return create_profile(
        db,
        current_user.id,
        profile_data,
    )


@router.get(
    "",
    response_model=FarmerProfileResponse,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = get_profile_by_user_id(
        db,
        current_user.id,
    )

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer profile not found",
        )

    return profile


@router.put(
    "",
    response_model=FarmerProfileResponse,
)
def update_my_profile(
    profile_data: FarmerProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = get_profile_by_user_id(
        db,
        current_user.id,
    )

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer profile not found",
        )

    return update_profile(
        db,
        profile,
        profile_data,
    )
