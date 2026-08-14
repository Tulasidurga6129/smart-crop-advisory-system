from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.farmer_profile import FarmerProfile
from app.schemas.farmer_profile import (
    FarmerProfileCreate,
    FarmerProfileUpdate,
)


def get_profile_by_user_id(
    db: Session,
    user_id: int,
) -> FarmerProfile | None:
    statement = select(FarmerProfile).where(
        FarmerProfile.user_id == user_id
    )

    return db.scalar(statement)


def create_profile(
    db: Session,
    user_id: int,
    profile_data: FarmerProfileCreate,
) -> FarmerProfile:
    profile = FarmerProfile(
        user_id=user_id,
        phone=profile_data.phone,
        address=profile_data.address,
        village=profile_data.village,
        district=profile_data.district,
        state=profile_data.state,
        land_area=profile_data.land_area,
        land_unit=profile_data.land_unit,
        primary_crop=profile_data.primary_crop,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


def update_profile(
    db: Session,
    profile: FarmerProfile,
    profile_data: FarmerProfileUpdate,
) -> FarmerProfile:
    update_data = profile_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile