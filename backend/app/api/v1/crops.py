from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.crop import Crop
from app.models.farm import Farm
from app.models.user import User
from app.schemas.crop import (
    CropCreate,
    CropResponse,
    CropUpdate,
)
from app.services.crop_service import (
    create_crop,
    delete_crop,
    get_crop_by_id,
    get_crops_by_farm_id,
    update_crop,
)
from app.services.crop_lifecycle_service import (
    get_crop_lifecycle,
)

router = APIRouter(
    prefix="/crops",
    tags=["Crops"],
)

def build_crop_response(crop):
    lifecycle = get_crop_lifecycle(
        crop_name=crop.name,
        sowing_date=crop.sowing_date,
        expected_harvest_date=crop.expected_harvest_date,
    )

    return {
        "id": crop.id,
        "farm_id": crop.farm_id,
        "name": crop.name,
        "variety": crop.variety,
        "season": crop.season,
        "sowing_date": crop.sowing_date,
        "expected_harvest_date": lifecycle[
            "expected_harvest_date"
        ],
        "area": crop.area,
        "status": crop.status,
        "crop_age_days": lifecycle[
            "crop_age_days"
        ],
        "growth_stage": lifecycle[
            "growth_stage"
        ],
        "days_to_harvest": lifecycle[
            "days_to_harvest"
        ],
    }

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
    "",
    response_model=CropResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_my_crop(
    crop_data: CropCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_my_farm(
        db,
        current_user,
        crop_data.farm_id,
    )

    crop = create_crop(
        db,
        crop_data,
    )

    return build_crop_response(crop)


@router.get(
    "/farm/{farm_id}",
    response_model=list[CropResponse],
)
def get_my_farm_crops(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_my_farm(
        db,
        current_user,
        farm_id,
    )

    crops = get_crops_by_farm_id(
    db,
    farm_id,
    )

    return [
        build_crop_response(crop)
        for crop in crops
    ]


@router.get(
    "/{crop_id}",
    response_model=CropResponse,
)
def get_my_crop(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crop = get_crop_by_id(
        db,
        crop_id,
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

    return build_crop_response(crop)


@router.put(
    "/{crop_id}",
    response_model=CropResponse,
)
def update_my_crop(
    crop_id: int,
    crop_data: CropUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crop = get_crop_by_id(
        db,
        crop_id,
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

    updated_crop = update_crop(
        db,
        crop,
        crop_data,
    )

    return build_crop_response(updated_crop)


@router.delete(
    "/{crop_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_crop(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crop = get_crop_by_id(
        db,
        crop_id,
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

    delete_crop(
        db,
        crop,
    )

    return None