from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.farm import Farm
from app.models.user import User
from app.schemas.weather import (
    WeatherCreate,
    WeatherResponse,
    WeatherUpdate,
)
from app.services.weather_service import (
    create_weather,
    delete_weather,
    get_weather_by_farm_id,
    get_weather_by_id,
    update_weather,
)


router = APIRouter(
    prefix="/weather",
    tags=["Weather"],
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


@router.post(
    "/farm/{farm_id}",
    response_model=WeatherResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_my_weather(
    farm_id: int,
    weather_data: WeatherCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_my_farm(
        db,
        current_user,
        farm_id,
    )

    return create_weather(
        db,
        farm_id,
        weather_data,
    )


@router.get(
    "/farm/{farm_id}",
    response_model=list[WeatherResponse],
)
def get_my_farm_weather(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_my_farm(
        db,
        current_user,
        farm_id,
    )

    return get_weather_by_farm_id(
        db,
        farm_id,
    )


@router.get(
    "/{weather_id}",
    response_model=WeatherResponse,
)
def get_my_weather(
    weather_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    weather = get_weather_by_id(
        db,
        weather_id,
    )

    if not weather:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather record not found",
        )

    get_my_farm(
        db,
        current_user,
        weather.farm_id,
    )

    return weather


@router.put(
    "/{weather_id}",
    response_model=WeatherResponse,
)
def update_my_weather(
    weather_id: int,
    weather_data: WeatherUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    weather = get_weather_by_id(
        db,
        weather_id,
    )

    if not weather:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather record not found",
        )

    get_my_farm(
        db,
        current_user,
        weather.farm_id,
    )

    return update_weather(
        db,
        weather,
        weather_data,
    )


@router.delete(
    "/{weather_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_weather(
    weather_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    weather = get_weather_by_id(
        db,
        weather_id,
    )

    if not weather:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather record not found",
        )

    get_my_farm(
        db,
        current_user,
        weather.farm_id,
    )

    delete_weather(
        db,
        weather,
    )

    return None