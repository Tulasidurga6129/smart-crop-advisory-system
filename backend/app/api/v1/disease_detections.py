from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
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
from app.services import disease_detection_service, disease_ml_service

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

@router.post(
    "/predict",
)
async def predict_disease(
    farm_id: int,
    crop_id: int,
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # -----------------------------------------------------
    # Verify farm belongs to current user
    # -----------------------------------------------------

    get_my_farm(
        db,
        current_user,
        farm_id,
    )

    # -----------------------------------------------------
    # Verify crop belongs to the specified farm
    # -----------------------------------------------------

    crop = (
        db.query(Crop)
        .filter(
            Crop.id == crop_id,
            Crop.farm_id == farm_id,
        )
        .first()
    )

    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found in the specified farm",
        )

    # -----------------------------------------------------
    # Validate image
    # -----------------------------------------------------

    if not image.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image content type is missing",
        )

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/jpg",
        "image/webp",
    }

    if image.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Unsupported image type. "
                "Use JPEG, PNG, JPG, or WEBP."
            ),
        )

    # -----------------------------------------------------
    # Read image
    # -----------------------------------------------------

    image_bytes = await image.read()

    if not image_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded image is empty",
        )

    # -----------------------------------------------------
    # Run ML prediction
    # -----------------------------------------------------

    try:
        prediction = disease_ml_service.predict_disease(
            image_bytes
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Disease detection failed: {exc}",
        )

    # -----------------------------------------------------
    # Save detection to database
    # -----------------------------------------------------

    detection_data = DiseaseDetectionCreate(
        farm_id=farm_id,
        crop_id=crop_id,
        disease_name=prediction["disease"],
        confidence=prediction["confidence"],
        severity="medium",
        symptoms=prediction["description"],
        recommended_treatment="\n".join(
            f"- {item}"
            for item in prediction["treatment"]
        ),
        preventive_measures="\n".join(
            f"- {item}"
            for item in prediction["prevention"]
        ),
        detection_source="ml",
        status="active",
    )

    detection = disease_detection_service.create_detection(
        db,
        detection_data,
    )

    # -----------------------------------------------------
    # Return prediction + saved detection
    # -----------------------------------------------------

    return {
        "detection": detection,
        "prediction": prediction,
        "image_filename": image.filename,
    }
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
