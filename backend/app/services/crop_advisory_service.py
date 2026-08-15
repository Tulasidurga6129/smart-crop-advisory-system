from datetime import datetime
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.crop_advisory import CropAdvisory
from app.schemas.crop_advisory import (
    CropAdvisoryCreate,
    CropAdvisoryUpdate,
)


def create_advisory(
    db: Session,
    advisory_data: CropAdvisoryCreate,
) -> CropAdvisory:
    advisory = CropAdvisory(
        farm_id=advisory_data.farm_id,
        crop_id=advisory_data.crop_id,
        advisory_type=advisory_data.advisory_type,
        title=advisory_data.title,
        message=advisory_data.message,
        priority=advisory_data.priority,
        status=advisory_data.status,
        valid_until=advisory_data.valid_until,
    )

    db.add(advisory)
    db.commit()
    db.refresh(advisory)

    return advisory


def get_advisory(
    db: Session,
    advisory_id: int,
) -> CropAdvisory | None:
    return (
        db.query(CropAdvisory)
        .filter(CropAdvisory.id == advisory_id)
        .first()
    )


def get_farm_advisories(
    db: Session,
    farm_id: int,
) -> list[CropAdvisory]:
    return (
        db.query(CropAdvisory)
        .filter(CropAdvisory.farm_id == farm_id)
        .order_by(CropAdvisory.created_at.desc())
        .all()
    )


def get_crop_advisories(
    db: Session,
    crop_id: int,
) -> list[CropAdvisory]:
    return (
        db.query(CropAdvisory)
        .filter(CropAdvisory.crop_id == crop_id)
        .order_by(CropAdvisory.created_at.desc())
        .all()
    )


def update_advisory(
    db: Session,
    advisory: CropAdvisory,
    advisory_data: CropAdvisoryUpdate,
) -> CropAdvisory:
    update_data = advisory_data.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(advisory, field, value)

    db.commit()
    db.refresh(advisory)

    return advisory


def delete_advisory(
    db: Session,
    advisory: CropAdvisory,
) -> None:
    db.delete(advisory)
    db.commit()
def get_active_farm_advisories(
    db: Session,
    farm_id: int,
) -> list[CropAdvisory]:
    now = datetime.utcnow()

    advisories = (
        db.query(CropAdvisory)
        .filter(
            CropAdvisory.farm_id == farm_id,
            CropAdvisory.status == "active",
            or_(
                CropAdvisory.valid_until.is_(None),
                CropAdvisory.valid_until > now,
            ),
        )
        .order_by(
            CropAdvisory.created_at.desc()
        )
        .all()
    )

    return advisories
def resolve_advisory(
    db: Session,
    advisory: CropAdvisory,
) -> CropAdvisory:
    advisory.status = "resolved"

    db.commit()
    db.refresh(advisory)

    return advisory


def dismiss_advisory(
    db: Session,
    advisory: CropAdvisory,
) -> CropAdvisory:
    advisory.status = "dismissed"

    db.commit()
    db.refresh(advisory)

    return advisory