import os
import sys


# Project root
PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
    )
)

ML_PATH = os.path.join(
    PROJECT_ROOT,
    "ml",
    "yield_prediction",
)

if ML_PATH not in sys.path:
    sys.path.insert(0, ML_PATH)


from yield_predictor import predict_yield


def predict_crop_yield(
    crop: str,
    crop_year: int,
    season: str,
    state: str,
    area: float,
    annual_rainfall: float,
    fertilizer: float,
    pesticide: float,
    avg_temperature: float,
    max_temperature: float,
    min_temperature: float,
) -> float:

    return predict_yield(
        crop=crop,
        crop_year=crop_year,
        season=season,
        state=state,
        area=area,
        annual_rainfall=annual_rainfall,
        fertilizer=fertilizer,
        pesticide=pesticide,
        avg_temperature=avg_temperature,
        max_temperature=max_temperature,
        min_temperature=min_temperature,
    )