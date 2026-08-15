from sqlalchemy.orm import Session

from app.models.disease_detection import DiseaseDetection
from app.schemas.disease_detection import (
    DiseaseDetectionCreate,
    DiseaseDetectionUpdate,
)


def create_detection(
    db: Session,
    detection_data: DiseaseDetectionCreate,
) -> DiseaseDetection:
    detection = DiseaseDetection(
        farm_id=detection_data.farm_id,
        crop_id=detection_data.crop_id,
        disease_name=detection_data.disease_name,
        confidence=detection_data.confidence,
        severity=detection_data.severity,
        symptoms=detection_data.symptoms,
        recommended_treatment=detection_data.recommended_treatment,
        preventive_measures=detection_data.preventive_measures,
        detection_source=detection_data.detection_source,
        status=detection_data.status,
    )

    db.add(detection)
    db.commit()
    db.refresh(detection)

    return detection


def get_detection(
    db: Session,
    detection_id: int,
) -> DiseaseDetection | None:
    return (
        db.query(DiseaseDetection)
        .filter(
            DiseaseDetection.id == detection_id,
        )
        .first()
    )


def get_farm_detections(
    db: Session,
    farm_id: int,
) -> list[DiseaseDetection]:
    return (
        db.query(DiseaseDetection)
        .filter(
            DiseaseDetection.farm_id == farm_id,
        )
        .order_by(
            DiseaseDetection.created_at.desc(),
        )
        .all()
    )


def get_crop_detections(
    db: Session,
    crop_id: int,
) -> list[DiseaseDetection]:
    return (
        db.query(DiseaseDetection)
        .filter(
            DiseaseDetection.crop_id == crop_id,
        )
        .order_by(
            DiseaseDetection.created_at.desc(),
        )
        .all()
    )


def update_detection(
    db: Session,
    detection: DiseaseDetection,
    detection_data: DiseaseDetectionUpdate,
) -> DiseaseDetection:
    update_data = detection_data.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(detection, field, value)

    db.commit()
    db.refresh(detection)

    return detection


def delete_detection(
    db: Session,
    detection: DiseaseDetection,
) -> None:
    db.delete(detection)
    db.commit()
