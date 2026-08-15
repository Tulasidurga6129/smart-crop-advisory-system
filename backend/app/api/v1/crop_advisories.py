from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.crop import Crop
from app.models.crop_advisory import CropAdvisory
from app.models.farm import Farm
from app.models.user import User
from app.schemas.crop_advisory import (
    CropAdvisoryCreate,
    CropAdvisoryResponse,
    CropAdvisoryUpdate,
)
from app.services import crop_advisory_service


router = APIRouter(
    prefix="/crop-advisories",
    tags=["Crop Advisories"],
)


def get_my_farm(
    db: Session,
    current_user: User,
    farm_id: int,
) -> Farm:
    farm = (
        db.query(Farm)
        .join(Farm.farmer_profile)
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


def get_my_advisory(
    db: Session,
    current_user: User,
    advisory_id: int,
) -> CropAdvisory:
    advisory = (
        db.query(CropAdvisory)
        .filter(
            CropAdvisory.id == advisory_id,
        )
        .first()
    )

    if not advisory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop advisory not found",
        )

    get_my_farm(
        db,
        current_user,
        advisory.farm_id,
    )

    return advisory


@router.post(
    "",
    response_model=CropAdvisoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_advisory(
    advisory_data: CropAdvisoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_my_farm(
        db,
        current_user,
        advisory_data.farm_id,
    )

    return crop_advisory_service.create_advisory(
        db,
        advisory_data,
    )


@router.get(
    "/farm/{farm_id}",
    response_model=list[CropAdvisoryResponse],
)
def get_farm_advisories(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_my_farm(
        db,
        current_user,
        farm_id,
    )

    return crop_advisory_service.get_farm_advisories(
        db,
        farm_id,
    )


@router.get(
    "/crop/{crop_id}",
    response_model=list[CropAdvisoryResponse],
)
def get_crop_advisories(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crop = (
        db.query(Crop)
        .filter(Crop.id == crop_id)
        .first()
    )

    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found",
        )

    get_my_farm(
        db,
        current_user,
        crop.farm_id,
    )

    return crop_advisory_service.get_crop_advisories(
        db,
        crop_id,
    )


@router.get(
    "/{advisory_id}",
    response_model=CropAdvisoryResponse,
)
def get_advisory(
    advisory_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_my_advisory(
        db,
        current_user,
        advisory_id,
    )


@router.put(
    "/{advisory_id}",
    response_model=CropAdvisoryResponse,
)
def update_advisory(
    advisory_id: int,
    advisory_data: CropAdvisoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    advisory = get_my_advisory(
        db,
        current_user,
        advisory_id,
    )

    return crop_advisory_service.update_advisory(
        db,
        advisory,
        advisory_data,
    )


@router.delete(
    "/{advisory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_advisory(
    advisory_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    advisory = get_my_advisory(
        db,
        current_user,
        advisory_id,
    )

    crop_advisory_service.delete_advisory(
        db,
        advisory,
    )

    return None