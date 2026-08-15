from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.crop_monitoring import (
    CropMonitoringCreate,
    CropMonitoringResponse,
    CropMonitoringUpdate,
)
from app.services.crop_monitoring_service import (
    create_monitoring,
    delete_monitoring,
    get_monitoring,
    get_monitoring_records,
    update_monitoring,
)


router = APIRouter(
    prefix="/crop-monitoring",
    tags=["Crop Monitoring"],
)


@router.post(
    "",
    response_model=CropMonitoringResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_crop_monitoring(
    monitoring_data: CropMonitoringCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    monitoring = create_monitoring(
        db=db,
        user_id=current_user.id,
        data=monitoring_data,
    )

    if not monitoring:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found or access denied",
        )

    return monitoring


@router.get(
    "/crop/{crop_id}",
    response_model=list[CropMonitoringResponse],
)
def get_crop_monitoring_records(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    records = get_monitoring_records(
        db=db,
        user_id=current_user.id,
        crop_id=crop_id,
    )

    if records is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found or access denied",
        )

    return records


@router.get(
    "/{monitoring_id}",
    response_model=CropMonitoringResponse,
)
def get_crop_monitoring(
    monitoring_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    monitoring = get_monitoring(
        db=db,
        user_id=current_user.id,
        monitoring_id=monitoring_id,
    )

    if not monitoring:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring record not found or access denied",
        )

    return monitoring


@router.put(
    "/{monitoring_id}",
    response_model=CropMonitoringResponse,
)
def update_crop_monitoring(
    monitoring_id: int,
    monitoring_data: CropMonitoringUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    monitoring = update_monitoring(
        db=db,
        user_id=current_user.id,
        monitoring_id=monitoring_id,
        data=monitoring_data,
    )

    if not monitoring:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring record not found or access denied",
        )

    return monitoring


@router.delete(
    "/{monitoring_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_crop_monitoring(
    monitoring_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deleted = delete_monitoring(
        db=db,
        user_id=current_user.id,
        monitoring_id=monitoring_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring record not found or access denied",
        )

    return None