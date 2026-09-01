from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.crop import Crop
from app.models.farm import Farm
from app.models.user import User
from app.schemas.yield_prediction import YieldPredictionResponse
from app.services.yield_prediction_service import (
    predict_yield_for_crop,
)


router = APIRouter(
    prefix="/yield-predictions",
    tags=["Yield Prediction"],
)


def get_my_crop(
    db: Session,
    current_user: User,
    crop_id: int,
) -> Crop:

    crop = (
        db.query(Crop)
        .join(Crop.farm)
        .join(Farm.farmer_profile)
        .filter(
            Crop.id == crop_id,
            Farm.farmer_profile.has(
                user_id=current_user.id
            ),
        )
        .first()
    )

    if not crop:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found",
        )

    return crop


@router.get(
    "/crop/{crop_id}",
    response_model=YieldPredictionResponse,
)
def predict_crop_yield(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    get_my_crop(
        db=db,
        current_user=current_user,
        crop_id=crop_id,
    )

    return predict_yield_for_crop(
        db=db,
        crop_id=crop_id,
    )