import os

import joblib
import pandas as pd


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "yield_model.pkl",
)


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

model = joblib.load(
    MODEL_PATH
)


# --------------------------------------------------
# Yield Prediction
# --------------------------------------------------

def predict_yield(
    crop,
    crop_year,
    season,
    state,
    area,
    annual_rainfall,
    avg_temperature,
    max_temperature,
    min_temperature,
):
    """
    Predict crop yield using automatically obtained
    weather/climate data and existing crop/farm data.
    """

    farmer_data = pd.DataFrame(
        [
            {
                "Crop": crop,
                "Crop_Year": crop_year,
                "Season": season,
                "State": state,
                "Area": area,
                "Annual_Rainfall": annual_rainfall,
                "Avg_Temperature": avg_temperature,
                "Max_Temperature": max_temperature,
                "Min_Temperature": min_temperature,
            }
        ]
    )

    prediction = model.predict(
        farmer_data
    )

    return float(
        prediction[0]
    )


# --------------------------------------------------
# Local Test
# --------------------------------------------------

if __name__ == "__main__":

    result = predict_yield(
        crop="Rice",
        crop_year=2025,
        season="Kharif",
        state="Andhra Pradesh",
        area=5000,
        annual_rainfall=1200,
        avg_temperature=27,
        max_temperature=35,
        min_temperature=21,
    )

    print(
        "Predicted Crop Yield:",
        round(result, 2),
    )