import joblib
import pandas as pd


# Load trained fertilizer recommendation model
model = joblib.load("fertilizer_model.pkl")


def predict_fertilizer(
    temperature,
    humidity,
    moisture,
    soil_type,
    crop_type,
    nitrogen,
    potassium,
    phosphorus
):
    input_data = pd.DataFrame([{
        "Temperature": temperature,
        "Humidity": humidity,
        "Moisture": moisture,
        "Soil Type": soil_type,
        "Crop Type": crop_type,
        "Nitrogen": nitrogen,
        "Potassium": potassium,
        "Phosphorus": phosphorus
    }])

    prediction = model.predict(input_data)

    return prediction[0]


# Test prediction
if __name__ == "__main__":

    result = predict_fertilizer(
        temperature=26,
        humidity=52,
        moisture=38,
        soil_type="Sandy",
        crop_type="Maize",
        nitrogen=37,
        potassium=0,
        phosphorus=0
    )

    print("Recommended Fertilizer:", result)