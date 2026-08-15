from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.crop import Crop
from app.models.disease_detection import DiseaseDetection
from app.models.farm import Farm
from app.models.user import User
from app.schemas.disease_detection import (
    DiseaseDetectionCreate,
    DiseaseDetectionResponse,
    DiseaseDetectionUpdate,
)
from app.services import disease_detection_service


router = APIRouter(
    prefix="/disease-detections",
    tags=["Disease Detection"],
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


def get_my_detection(
    db: Session,
    current_user: User,
    detection_id: int,
) -> DiseaseDetection:
    detection = (
        db.query(DiseaseDetection)
        .filter(
            DiseaseDetection.id == detection_id,
        )
        .first()
    )

    if not detection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disease detection not found",
        )

    get_my_farm(
        db,
        current_user,
        detection.farm_id,
    )

    return detection


@router.post(
    "",
    response_model=DiseaseDetectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_detection(
    detection_data: DiseaseDetectionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_my_farm(
        db,
        current_user,
        detection_data.farm_id,
    )

    crop = (
        db.query(Crop)
        .filter(
            Crop.id == detection_data.crop_id,
            Crop.farm_id == detection_data.farm_id,
        )
        .first()
    )

    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found in the specified farm",
        )

    return disease_detection_service.create_detection(
        db,
        detection_data,
    )


@router.get(
    "/farm/{farm_id}",
    response_model=list[DiseaseDetectionResponse],
)
def get_farm_detections(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_my_farm(
        db,
        current_user,
        farm_id,
    )

    return disease_detection_service.get_farm_detections(
        db,
        farm_id,
    )


@router.get(
    "/crop/{crop_id}",
    response_model=list[DiseaseDetectionResponse],
)
def get_crop_detections(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    crop = (
        db.query(Crop)
        .filter(
            Crop.id == crop_id,
        )
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

    return disease_detection_service.get_crop_detections(
        db,
        crop_id,
    )


@router.get(
    "/{detection_id}",
    response_model=DiseaseDetectionResponse,
)
def get_detection(
    detection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_my_detection(
        db,
        current_user,
        detection_id,
    )


@router.put(
    "/{detection_id}",
    response_model=DiseaseDetectionResponse,
)
def update_detection(
    detection_id: int,
    detection_data: DiseaseDetectionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    detection = get_my_detection(
        db,
        current_user,
        detection_id,
    )

    return disease_detection_service.update_detection(
        db,
        detection,
        detection_data,
    )


@router.delete(
    "/{detection_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_detection(
    detection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    detection = get_my_detection(
        db,
        current_user,
        detection_id,
    )

    disease_detection_service.delete_detection(
        db,
        detection,
    )

    return None
