from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.weather import Weather
from app.schemas.weather import WeatherCreate, WeatherUpdate


def create_weather(
    db: Session,
    farm_id: int,
    weather_data: WeatherCreate,
) -> Weather:
    weather = Weather(
        farm_id=farm_id,
        **weather_data.model_dump(
            exclude_unset=True
        ),
    )

    db.add(weather)
    db.commit()
    db.refresh(weather)

    return weather


def get_weather_by_id(
    db: Session,
    weather_id: int,
) -> Weather | None:
    statement = select(Weather).where(
        Weather.id == weather_id
    )

    return db.scalar(statement)


def get_weather_by_farm_id(
    db: Session,
    farm_id: int,
) -> list[Weather]:
    statement = (
        select(Weather)
        .where(
            Weather.farm_id == farm_id
        )
        .order_by(
            Weather.observed_at.desc()
        )
    )

    return list(
        db.scalars(statement).all()
    )


def update_weather(
    db: Session,
    weather: Weather,
    weather_data: WeatherUpdate,
) -> Weather:
    update_data = weather_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(weather, field, value)

    db.commit()
    db.refresh(weather)

    return weather


def delete_weather(
    db: Session,
    weather: Weather,
) -> None:
    db.delete(weather)
    db.commit()