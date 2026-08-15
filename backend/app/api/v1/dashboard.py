from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.farm import Farm
from app.models.user import User
from app.schemas.dashboard import FarmDashboardResponse
from app.services.dashboard_service import get_farm_dashboard


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
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


@router.get(
    "/farm/{farm_id}",
    response_model=FarmDashboardResponse,
)
def get_my_farm_dashboard(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    farm = get_my_farm(
        db,
        current_user,
        farm_id,
    )

    return get_farm_dashboard(
        db,
        farm,
    )