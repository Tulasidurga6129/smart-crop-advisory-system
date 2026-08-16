from fertilizer_predictor import predict_fertilizer


test_cases = [
    {
        "temperature": 26,
        "humidity": 52,
        "moisture": 38,
        "soil_type": "Sandy",
        "crop_type": "Maize",
        "nitrogen": 37,
        "potassium": 0,
        "phosphorus": 0
    },
    {
        "temperature": 29,
        "humidity": 52,
        "moisture": 45,
        "soil_type": "Loamy",
        "crop_type": "Sugarcane",
        "nitrogen": 12,
        "potassium": 0,
        "phosphorus": 36
    },
    {
        "temperature": 34,
        "humidity": 65,
        "moisture": 62,
        "soil_type": "Black",
        "crop_type": "Cotton",
        "nitrogen": 7,
        "potassium": 9,
        "phosphorus": 30
    },
    {
        "temperature": 32,
        "humidity": 62,
        "moisture": 34,
        "soil_type": "Red",
        "crop_type": "Wheat",
        "nitrogen": 22,
        "potassium": 0,
        "phosphorus": 20
    },
    {
        "temperature": 28,
        "humidity": 54,
        "moisture": 46,
        "soil_type": "Clayey",
        "crop_type": "Paddy",
        "nitrogen": 35,
        "potassium": 0,
        "phosphorus": 0
    }
]


print("\nFertilizer Recommendation Testing")
print("=" * 50)

for i, case in enumerate(test_cases, start=1):

    fertilizer = predict_fertilizer(
        temperature=case["temperature"],
        humidity=case["humidity"],
        moisture=case["moisture"],
        soil_type=case["soil_type"],
        crop_type=case["crop_type"],
        nitrogen=case["nitrogen"],
        potassium=case["potassium"],
        phosphorus=case["phosphorus"]
    )

    print(f"\nTest {i}")
    print(f"Crop: {case['crop_type']}")
    print(f"Soil: {case['soil_type']}")
    print(f"N: {case['nitrogen']}, K: {case['potassium']}, P: {case['phosphorus']}")
    print(f"Recommended Fertilizer: {fertilizer}")