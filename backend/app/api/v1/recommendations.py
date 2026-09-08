from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.crop import Crop
from app.models.farm import Farm
from app.models.user import User
from app.services.recommendation_service import (
    create_recommendations,
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


def get_my_crop(
    db: Session,
    current_user: User,
    crop_id: int,
) -> Crop:
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

    farm = (
        db.query(Farm)
        .join(Farm.farmer_profile)
        .filter(
            Farm.id == crop.farm_id,
            Farm.farmer_profile.has(
                user_id=current_user.id
            ),
        )
        .first()
    )

    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found",
        )

    return crop


@router.post(
    "/{crop_id}",
)
def generate_crop_recommendations(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crop = get_my_crop(
        db,
        current_user,
        crop_id,
    )

    farm = (
        db.query(Farm)
        .filter(Farm.id == crop.farm_id)
        .first()
    )

    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found",
        )

    recommendations = create_recommendations(
    db,
    farm,
    crop,
    current_user.id,
)

    return [
    {
        "id": advisory.id,
        "farm_id": advisory.farm_id,
        "crop_id": advisory.crop_id,
        "advisory_type": advisory.advisory_type,
        "title": advisory.title,
        "message": advisory.message,
        "priority": advisory.priority,
        "status": advisory.status,
        "valid_until": advisory.valid_until,
        "created_at": advisory.created_at,
    }
    for advisory in recommendations
]