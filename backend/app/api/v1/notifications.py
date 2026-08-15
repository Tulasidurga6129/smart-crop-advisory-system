from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
    NotificationUpdate,
)
from app.services import notification_service


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


def get_my_notification(
    db: Session,
    current_user: User,
    notification_id: int,
) -> Notification:
    notification = notification_service.get_notification(
        db,
        notification_id,
        current_user.id,
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    return notification


@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_notification(
    notification_data: NotificationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return notification_service.create_notification(
        db,
        current_user.id,
        notification_data,
    )


@router.get(
    "",
    response_model=list[NotificationResponse],
)
def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return notification_service.get_user_notifications(
        db,
        current_user.id,
    )


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def get_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_my_notification(
        db,
        current_user,
        notification_id,
    )


@router.put(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def update_notification(
    notification_id: int,
    notification_data: NotificationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notification = get_my_notification(
        db,
        current_user,
        notification_id,
    )

    return notification_service.update_notification(
        db,
        notification,
        notification_data,
    )


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notification = get_my_notification(
        db,
        current_user,
        notification_id,
    )

    return notification_service.mark_notification_as_read(
        db,
        notification,
    )


@router.patch(
    "/read-all",
    status_code=status.HTTP_204_NO_CONTENT,
)
def mark_all_notifications_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notification_service.mark_all_notifications_as_read(
        db,
        current_user.id,
    )

    return None


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notification = get_my_notification(
        db,
        current_user,
        notification_id,
    )

    notification_service.delete_notification(
        db,
        notification,
    )

    return None