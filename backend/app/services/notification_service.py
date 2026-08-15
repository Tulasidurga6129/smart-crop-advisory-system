from datetime import datetime

from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
)


def create_notification(
    db: Session,
    user_id: int,
    notification_data: NotificationCreate,
) -> Notification:
    notification = Notification(
        user_id=user_id,
        farm_id=notification_data.farm_id,
        crop_id=notification_data.crop_id,
        notification_type=notification_data.notification_type,
        title=notification_data.title,
        message=notification_data.message,
        priority=notification_data.priority,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


def get_notification(
    db: Session,
    notification_id: int,
    user_id: int,
) -> Notification | None:
    return (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == user_id,
        )
        .first()
    )


def get_user_notifications(
    db: Session,
    user_id: int,
) -> list[Notification]:
    return (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id,
        )
        .order_by(
            Notification.created_at.desc(),
        )
        .all()
    )


def update_notification(
    db: Session,
    notification: Notification,
    notification_data: NotificationUpdate,
) -> Notification:
    update_data = notification_data.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(notification, field, value)

    db.commit()
    db.refresh(notification)

    return notification


def mark_notification_as_read(
    db: Session,
    notification: Notification,
) -> Notification:
    notification.is_read = True
    notification.read_at = datetime.utcnow()

    db.commit()
    db.refresh(notification)

    return notification


def mark_all_notifications_as_read(
    db: Session,
    user_id: int,
) -> None:
    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id,
            Notification.is_read.is_(False),
        )
        .all()
    )

    read_time = datetime.utcnow()

    for notification in notifications:
        notification.is_read = True
        notification.read_at = read_time

    db.commit()


def delete_notification(
    db: Session,
    notification: Notification,
) -> None:
    db.delete(notification)
    db.commit()