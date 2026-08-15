import os
import pandas as pd
import joblib

# Get the folder where this Python file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to trained model
MODEL_PATH = os.path.join(BASE_DIR, "yield_model.pkl")

# Load trained model
model = joblib.load(MODEL_PATH)


def predict_yield(
    crop,
    crop_year,
    season,
    state,
    area,
    annual_rainfall,
    fertilizer,
    pesticide,
    avg_temperature,
    max_temperature,
    min_temperature
):

    farmer_data = pd.DataFrame([{
        "Crop": crop,
        "Crop_Year": crop_year,
        "Season": season,
        "State": state,
        "Area": area,
        "Annual_Rainfall": annual_rainfall,
        "Fertilizer": fertilizer,
        "Pesticide": pesticide,
        "Avg_Temperature": avg_temperature,
        "Max_Temperature": max_temperature,
        "Min_Temperature": min_temperature
    }])

    prediction = model.predict(farmer_data)

    return float(prediction[0])


# Test the model
if __name__ == "__main__":

    result = predict_yield(
        crop="Rice",
        crop_year=2025,
        season="Kharif",
        state="Andhra Pradesh",
        area=5000,
        annual_rainfall=1200,
        fertilizer=150000,
        pesticide=500,
        avg_temperature=27,
        max_temperature=35,
        min_temperature=21
    )

    print("Predicted Crop Yield:", round(result, 2))