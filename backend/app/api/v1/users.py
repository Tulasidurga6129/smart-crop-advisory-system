from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, require_roles

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.get("/admin-test")
def admin_test(
    current_user: User = Depends(require_roles("ADMIN")),
):
    return {
        "message": "Admin access granted",
        "user": current_user.name,
        "role": current_user.role,
    }